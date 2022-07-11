import type { HexbinBin } from 'd3-hexbin';
import { hexbin } from "d3-hexbin";
import type { ScaleLinear } from 'd3-scale';
import { writable } from 'svelte/store';

import { groundTruthData } from '$lib/state/ground-truth-data';
import { primarySample, secondarySample } from '$lib/state/sampled-data';
import { scaleX, scaleY } from '$lib/state/scales';
import { selectedBins } from '$lib/state/selected-bin';
import { globalViewConfig } from '$lib/state/view-config';
import { currentTransform } from '$lib/state/zoom';

type BinType = [number, number, number]; // x, y, id

export const hexbinning = hexbin<BinType>();

export const primaryBins = writable([] as HexbinBin<BinType>[]);
export const secondaryBins = writable([] as HexbinBin<BinType>[]);

export const primaryData = writable([] as number[][]);
export const secondaryData = writable([] as number[][]);

export const selectedPrimaryIds = writable([]);
export const selectedSecondaryIds = writable([]);

class BinGenerator {
  private _groundTruthData: number[][] = [];
  private _primaryData: number[][] = [];
  private _secondaryData: number[][] = [];

  private _groundTruthDataMap: Map<number, number[]> = new Map();
  private _primaryDataMap: Map<number, number[]> = new Map();
  private _secondaryDataMap: Map<number, number[]> = new Map();

  private _groundTruthBins: HexbinBin<BinType>[];
  private _primaryBins: HexbinBin<BinType>[];
  private _secondaryBins: HexbinBin<BinType>[];
  private _differenceBins;

  private _groundTruthIndex = {};
  private _primaryIndex = {};
  private _secondaryIndex = {};
  private _differenceIndex = {};

  private scaleX: ScaleLinear<number, number>;
  private scaleY: ScaleLinear<number, number>;

  private X: string;
  private Y: string;

  constructor() {
    groundTruthData.subscribe(value => {
      this._groundTruthData = value;
      this.insertDataIntoMap(value, this._groundTruthDataMap);
      this.updatePrimaryBins();
    });
    primarySample.subscribe(value => {
      this.primaryData = value.slice(0);
    });
    secondarySample.subscribe(value => {
      this.secondaryData = value.slice(0);
    });

    selectedBins.subscribe(value => {
      selectedPrimaryIds.set(value
        .map(bin => this.getPrimaryBin([bin.x, bin.y, -1])?.map(item => item[2])).flat());

      selectedSecondaryIds.set(value
        .map(bin => this.getSecondaryBin([bin.x, bin.y, -1])?.map(item => item[2])).flat());
    });

    scaleX.subscribe(value => this.scaleX = value);
    scaleY.subscribe(value => this.scaleY = value);

    currentTransform.subscribe(() => {
      // transform updates scales
      hexbinning
        .x(d => this.scaleX(d[0]))
        .y(d => this.scaleY(d[1]));

      this.updatePrimaryBins();
      this.updateSecondaryBins();
      this.updateGroundTruthBins();
    });

    globalViewConfig.subscribe(value => {
      hexbinning.radius(value.binSize);
      this.updatePrimaryBins();
      this.updateSecondaryBins();
      this.updateGroundTruthBins();
      this.X = value.encoding.x;
      this.Y = value.encoding.y;
    });
  }

  private getIndexForBins(bins: HexbinBin<BinType>[]) {
    const index = {};
    bins.forEach(bin => {
      if (index[bin.x] === undefined) {
        index[bin.x] = {};
      }

      index[bin.x][bin.y] = bin;
    });
    return index;
  }

  private getDifferenceWhereExistInPrimary(primaryIndex, secondaryIndex, relativeDifference=false) {
    Object.keys(primaryIndex).forEach(level1Key => {
      this._differenceIndex[level1Key] = {};

      if (secondaryIndex[level1Key] === undefined) {
        Object.keys(primaryIndex[level1Key]).forEach(level2Key => {
          if (relativeDifference) {
            this._differenceIndex[level1Key][level2Key] = 1;
          } else {
            this._differenceIndex[level1Key][level2Key] = primaryIndex[level1Key][level2Key].length;
          }
        });
      } else {
        Object.keys(primaryIndex[level1Key]).forEach(level2Key => {
          if (secondaryIndex[level1Key][level2Key] === undefined) {
            if (relativeDifference) {
              this._differenceIndex[level1Key][level2Key] = 1;
            } else {
              this._differenceIndex[level1Key][level2Key] = primaryIndex[level1Key][level2Key].length;
            }
          } else {
            if (relativeDifference) {
              const primary = primaryIndex[level1Key][level2Key].length;
              const secondary = secondaryIndex[level1Key][level2Key].length;
              this._differenceIndex[level1Key][level2Key] = (secondary - primary) / -Math.max(primary, secondary);
            } else {
              this._differenceIndex[level1Key][level2Key] = primaryIndex[level1Key][level2Key].length - secondaryIndex[level1Key][level2Key].length;
            }
          }
        });
      }
    });
  }

  private getDifferenceWhereExistInSecondaryOnly(secondaryIndex, relativeDifference=false) {
    Object.keys(secondaryIndex).forEach(level1Key => {
      if (this._differenceIndex[level1Key] === undefined) {
        this._differenceIndex[level1Key] = {};
        Object.keys(secondaryIndex[level1Key]).forEach(level2Key => {
          if (relativeDifference) {
            this._differenceIndex[level1Key][level2Key] = -1;
          } else {
            this._differenceIndex[level1Key][level2Key] = -secondaryIndex[level1Key][level2Key].length;
          }
        });
      } else {
        Object.keys(secondaryIndex[level1Key]).forEach(level2Key => {
          if (this._differenceIndex[level1Key][level2Key] === undefined) {
            if (relativeDifference) {
              this._differenceIndex[level1Key][level2Key] = -1;
            } else {
              this._differenceIndex[level1Key][level2Key] = -secondaryIndex[level1Key][level2Key].length;
            }
          }
        });
      }
    });
  }

  private unravelIndexIntoBins() {
    const differenceBins = [];

    Object.keys(this._differenceIndex).forEach(level1Key => {
      Object.keys(this._differenceIndex[level1Key]).forEach(level2Key => {
        differenceBins.push({
          x: +level1Key,
          y: +level2Key,
          length: this._differenceIndex[level1Key][level2Key]
        });
      });
    });

    return differenceBins;
  }

  public getDifferenceBins(relativeDifference=false,
                           isLeftGroundTruth=false,
                           isRightGroundTruth=false): HexbinBin<BinType>[] {
    this._differenceIndex = {};

    // first, compute the difference between the two indeces for all bins that exist in primary

    if (isLeftGroundTruth) {
      this.getDifferenceWhereExistInPrimary(
        this._groundTruthIndex, this._secondaryIndex, relativeDifference
      );
    } else if (isRightGroundTruth) {
      this.getDifferenceWhereExistInPrimary(
        this._primaryIndex, this._groundTruthIndex, relativeDifference
      );
    } else {
      this.getDifferenceWhereExistInPrimary(
        this._primaryIndex, this._secondaryIndex, relativeDifference
      );
    }

    // then, for all bins that only exist in secondary, store these as well
    if (isRightGroundTruth) {
      this.getDifferenceWhereExistInSecondaryOnly(this._groundTruthIndex, relativeDifference);
    } else {
      this.getDifferenceWhereExistInSecondaryOnly(this._secondaryIndex, relativeDifference);
    }

    // unravel the differenceIndex into HexbinBins again.
    this._differenceBins = this.unravelIndexIntoBins();

    return this._differenceBins;
  }

  private insertDataIntoMap(data: number[][], map: Map<number, number[]>) {
    data.forEach(datum => {
      map.set(datum[0], datum);
    });
  }

  private updateGroundTruthBins() {
    this._groundTruthBins = hexbinning(this._groundTruthData.map(d => [d[this.X], d[this.Y], d[0]]));
    this._groundTruthIndex = this.getIndexForBins(this._groundTruthBins)
  }

  private updatePrimaryBins() {
    this._primaryBins = hexbinning(this._primaryData.map(d => [d[this.X], d[this.Y], d[0]]));
    primaryBins.set(this._primaryBins);
    this._primaryIndex = this.getIndexForBins(this._primaryBins);
  }

  private updateSecondaryBins() {
    this._secondaryBins = hexbinning(this._secondaryData.map(d => [d[this.X], d[this.Y], d[0]]));
    secondaryBins.set(this._secondaryBins);
    this._secondaryIndex = this.getIndexForBins(this._secondaryBins);
  }

  public get primaryData(): number[][] {
    return this._primaryData;
  }

  public set primaryData(data: number[][]) {
    this._primaryData = data;
    this.insertDataIntoMap(data, this._primaryDataMap);
    primaryData.set(data);

    this.updatePrimaryBins();
  }

  public get secondaryData(): number[][] {
    return this._secondaryData;
  }

  public set secondaryData(data: number[][]) {
    this._secondaryData = data;
    this.insertDataIntoMap(data, this._secondaryDataMap);
    secondaryData.set(data);

    this.updateSecondaryBins();
  }

  // x and y are plot coordinates!
  public getPrimaryBin(bin: BinType): HexbinBin<BinType> {
    if (this._primaryIndex[bin[0]] === undefined) {
      return null;
    }

    return this._primaryIndex[bin[0]][bin[1]];
  }

  public getPrimaryBinForScreenPosition(x: number, y: number): HexbinBin<BinType> {
    const bin = hexbinning([[x, y, -1]])[0];
    return this.getPrimaryBin([bin.x, bin.y, -1]);
  }

  public getSecondaryBin(bin: BinType): HexbinBin<BinType> {
    if (this._secondaryIndex[bin[0]] === undefined) {
      return null;
    }

    return this._secondaryIndex[bin[0]][bin[1]];
  }

  public getSecondaryBinForScreenPosition(x: number, y: number): HexbinBin<BinType> {
    const bin = hexbinning([[x, y, -1]])[0];
    return this.getSecondaryBin([bin.x, bin.y, -1]);
  }

  public getDifferenceBin(bin: BinType): HexbinBin<BinType> {
    if (this._differenceBins[bin[0]] === undefined) {
      return null;
    }

    return this._differenceBins[bin[0]][bin[1]];
  }

  public getDifferenceBinForScreenPosition(x: number, y: number): HexbinBin<BinType> {
    const bin = hexbinning([[x, y, -1]])[0];
    return this.getDifferenceBin([bin.x, bin.y, -1]);
  }

  public getPrimaryDatum(id: number): number[] {
    return this._primaryDataMap.get(id);
  }

  public getPrimaryDataList(ids: number[]): number[][] {
    return ids.map(id => this.getPrimaryDatum(id));
  }

  public getSecondaryDatum(id: number): number[] {
    return this._secondaryDataMap.get(id);
  }

  public getSecondaryDataList(ids: number[]): number[][] {
    return ids.map(id => this.getSecondaryDatum(id));
  }
}

export type { BinGenerator };
export type { BinType };
export const generator = new BinGenerator();