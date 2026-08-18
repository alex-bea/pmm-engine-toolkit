// JS fixture — contains functions of varying sizes to exercise the walker.

function small(a, b) {
  return a + b;
}

const arrowSmall = (x) => x * 2;

const arrowLong = (n) => {
  let total = 0;
  total += 1;
  total += 2;
  total += 3;
  total += 4;
  total += 5;
  total += 6;
  total += 7;
  total += 8;
  total += 9;
  return total + n;
};

const obj = {
  methodShort: function () {
    return 1;
  },
};
