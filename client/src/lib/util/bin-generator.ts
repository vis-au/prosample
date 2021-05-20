import type { HexbinBin } from 'd3-hexbin';
import { hexbin } from "d3-hexbin";
import { writable } from 'svelte/store';

export const hexbinning = hexbin<[number, number]>()
  .radius(10);
export const hexagon = hexbinning.hexagon();

export const primaryBins = writable([] as HexbinBin<[number, number]>[]);
export const secondaryBins = writable([] as HexbinBin<[number, number]>[]);


class BinGenerator {
  private _primaryData: number[][] = [];
  private _secondaryData: number[][] = [];

  private _primaryBins: HexbinBin<[number, number]>[];
  private _secondaryBins: HexbinBin<[number, number]>[];
  private _differenceBins;

  private _primaryIndex = {};
  private _secondaryIndex = {};
  private _differenceIndex = {};

  private getIndexForBins(bins: HexbinBin<[number, number]>[]) {
    const index: any = {};
    bins.forEach(bin => {
      if (index[bin.x] === undefined) {
        index[bin.x] = {};
      }

      index[bin.x][bin.y] = bin;
    });
    return index;
  }

  private getDifferenceWhereExistInPrimary(primaryIndex, secondaryIndex) {
    Object.keys(primaryIndex).forEach(level1Key => {
      this._differenceIndex[level1Key] = {};

      if (secondaryIndex[level1Key] === undefined) {
        Object.keys(primaryIndex[level1Key]).forEach(level2key => {
          this._differenceIndex[level1Key][level2key] = primaryIndex[level1Key][level2key].length;
        });
      } else {
        Object.keys(primaryIndex[level1Key]).forEach(level2key => {
          if (secondaryIndex[level1Key][level2key] === undefined) {
            this._differenceIndex[level1Key][level2key] = primaryIndex[level1Key][level2key].length;
          } else {
            this._differenceIndex[level1Key][level2key] = primaryIndex[level1Key][level2key].length - secondaryIndex[level1Key][level2key].length;
          }
        });
      }
    });
  }

  private getDifferenceWhereExistInSecondaryOnly(secondaryIndex) {
    Object.keys(secondaryIndex).forEach(level1Key => {
      if (this._differenceIndex[level1Key] === undefined) {
        this._differenceIndex[level1Key] = {};
        Object.keys(secondaryIndex[level1Key]).forEach(level2Key => {
          this._differenceIndex[level1Key][level2Key] = -secondaryIndex[level1Key][level2Key].length;
        });
      } else {
        Object.keys(secondaryIndex[level1Key]).forEach(level2Key => {
          if (this._differenceIndex[level1Key][level2Key] === undefined) {
            this._differenceIndex[level1Key][level2Key] = -secondaryIndex[level1Key][level2Key].length;
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

  public getDifferenceBins() {
    this._differenceIndex = {};

    // first, compute the difference between the two indeces for all bins that exist in primary
    this.getDifferenceWhereExistInPrimary(this._primaryIndex, this._secondaryIndex);

    // then, for all bins that only exist in secondary, store these as well
    this.getDifferenceWhereExistInSecondaryOnly(this._secondaryIndex);

    // unravel the differenceIndex into HexbinBins again.
    this._differenceBins = this.unravelIndexIntoBins();

    return this._differenceBins;
  }

  public get primaryData() {
    return this._primaryData;
  }
  public set primaryData(data: number[][]) {
    this._primaryData = data;
    this._primaryBins = hexbinning(data.map(d => [d[1], d[2]]));
    primaryBins.set(this._primaryBins);
    this._primaryIndex = this.getIndexForBins(this._primaryBins);
  }

  public get secondaryData() {
    return this._secondaryData;
  }

  public set secondaryData(data: number[][]) {
    this._secondaryData = data;
    this._secondaryBins = hexbinning(data.map(d => [d[1], d[2]]));
    secondaryBins.set(this._secondaryBins);
    this._secondaryIndex = this.getIndexForBins(this._secondaryBins);
  }

  // x and y are plot coordinates!
  public getPrimaryBin(x: number, y: number) {
    const bin = hexbinning([[x, y]])[0];

    if (this._primaryIndex[bin.x] === undefined) {
      return null;
    }

    return this._primaryIndex[bin.x][bin.y];
  }

  public getSecondaryBin(x: number, y: number) {
    const bin = hexbinning([[x, y]])[0];

    if (this._secondaryIndex[bin.x] === undefined) {
      return null;
    }

    return this._secondaryIndex[bin.x][bin.y]
  }

  public getDifferenceBin(x: number, y: number) {
    const bin = hexbinning([[x, y]])[0];

    return this._differenceBins[bin.x][bin.y];
  }
}

export type { BinGenerator };
export const generator = new BinGenerator();