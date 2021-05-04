import type { HexbinBin } from 'd3-hexbin';


function getIndexForBins(bins: HexbinBin<[number, number]>[]) {
  const index: any = {};
  bins.forEach(bin => {
    if (index[bin.x] === undefined) {
      index[bin.x] = {};
    }

    index[bin.x][bin.y] = bin.length;
  });
  return index;
}

function getDifferenceWhereExistInPrimary(primaryIndex, secondaryIndex, differenceIndex) {
  Object.keys(primaryIndex).forEach(level1Key => {
    differenceIndex[level1Key] = {};

    if (secondaryIndex[level1Key] === undefined) {
      Object.keys(primaryIndex[level1Key]).forEach(level2key => {
        differenceIndex[level1Key][level2key] = primaryIndex[level1Key][level2key];
      });
    } else {
      Object.keys(primaryIndex[level1Key]).forEach(level2key => {
        if (secondaryIndex[level1Key][level2key] === undefined) {
          differenceIndex[level1Key][level2key] = primaryIndex[level1Key][level2key];
        } else {
          differenceIndex[level1Key][level2key] = primaryIndex[level1Key][level2key] - secondaryIndex[level1Key][level2key] ;
        }
      });
    }
  });
}

function getDifferenceWhereExistInSecondaryOnly(secondaryIndex, differenceIndex) {
  Object.keys(secondaryIndex).forEach(level1Key => {
    if (differenceIndex[level1Key] === undefined) {
      differenceIndex[level1Key] = {};
      Object.keys(secondaryIndex[level1Key]).forEach(level2Key => {
        differenceIndex[level1Key][level2Key] = -secondaryIndex[level1Key][level2Key];
      });
    } else {
      Object.keys(secondaryIndex[level1Key]).forEach(level2Key => {
        if (differenceIndex[level1Key][level2Key] === undefined) {
          differenceIndex[level1Key][level2Key] = -secondaryIndex[level1Key][level2Key];
        }
      });
    }
  });
}

function unravelIndexIntoBins(differenceIndex) {
  const differenceBins = [];

  Object.keys(differenceIndex).forEach(level1Key => {
    Object.keys(differenceIndex[level1Key]).forEach(level2Key => {
      differenceBins.push({
        x: +level1Key,
        y: +level2Key,
        length: differenceIndex[level1Key][level2Key]
      });
    });
  });

  return differenceBins;
}

export function getDifferenceBins(primaryBins, secondaryBins) {
  const primaryIndex = getIndexForBins(primaryBins);
  const secondaryIndex = getIndexForBins(secondaryBins);

  const differenceIndex: any = {};

  // first, compute the difference between the two indeces for all bins that exist in primary
  getDifferenceWhereExistInPrimary(primaryIndex, secondaryIndex, differenceIndex);

  // then, for all bins that only exist in secondary, store these as well
  getDifferenceWhereExistInSecondaryOnly(secondaryIndex, differenceIndex);

  // unravel the differenceIndex into HexbinBins again.
  const differenceBins = unravelIndexIntoBins(differenceIndex);

  return differenceBins;
}