import type { HexbinBin } from 'd3-hexbin';
import { hexbin } from "d3-hexbin";
import { writable } from 'svelte/store';

export const hexbinning = hexbin<BinType>()
  .radius(10);
export const hexagon = hexbinning.hexagon();

export const primaryBins = writable([] as HexbinBin<BinType>[]);
export const secondaryBins = writable([] as HexbinBin<BinType>[]);

export const primaryData = writable([] as number[][]);
export const secondaryData = writable([] as number[][]);

type BinType = [number, number, number]; // x, y, id

class BinGenerator {
  private _primaryData: number[][] = [];
  private _secondaryData: number[][] = [];

  private _primaryDataMap: Map<number, number[]> = new Map();
  private _secondaryDataMap: Map<number, number[]> = new Map();

  private _primaryBins: HexbinBin<BinType>[];
  private _secondaryBins: HexbinBin<BinType>[];
  private _differenceBins;

  private _primaryIndex = {};
  private _secondaryIndex = {};
  private _differenceIndex = {};

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

  public getDifferenceBins(relativeDifference=false): HexbinBin<BinType>[] {
    this._differenceIndex = {};

    // first, compute the difference between the two indeces for all bins that exist in primary
    this.getDifferenceWhereExistInPrimary(this._primaryIndex, this._secondaryIndex, relativeDifference);

    // then, for all bins that only exist in secondary, store these as well
    this.getDifferenceWhereExistInSecondaryOnly(this._secondaryIndex, relativeDifference);

    // unravel the differenceIndex into HexbinBins again.
    this._differenceBins = this.unravelIndexIntoBins();

    return this._differenceBins;
  }

  private insertDataIntoMap(data: number[][], map: Map<number, number[]>) {
    data.forEach(datum => {
      map.set(datum[0], datum);
    });
  }

  public get primaryData(): number[][] {
    return this._primaryData;
  }

  public set primaryData(data: number[][]) {
    this._primaryData = data;
    this.insertDataIntoMap(data, this._primaryDataMap);
    primaryData.set(data);
    this._primaryBins = hexbinning(data.map(d => [d[1], d[2], d[0]]));
    primaryBins.set(this._primaryBins);
    this._primaryIndex = this.getIndexForBins(this._primaryBins);
  }

  public get secondaryData(): number[][] {
    return this._secondaryData;
  }

  public set secondaryData(data: number[][]) {
    this._secondaryData = data;
    this.insertDataIntoMap(data, this._secondaryDataMap);
    secondaryData.set(data);
    this._secondaryBins = hexbinning(data.map(d => [d[1], d[2], d[0]]));
    secondaryBins.set(this._secondaryBins);
    this._secondaryIndex = this.getIndexForBins(this._secondaryBins);
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