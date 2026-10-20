// Clamp Math engine: fluid text size arithmetic for CSS clamp(). The formula between two sizes and two viewport widths, the size at a width, and the width that gives a size. Exact integers, results rounded half up.
function _int(t, err, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  if (!/^[0-9]{1,5}$/.test(t)) throw new Error(err);
  var v = parseInt(t, 10);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
function _fl(n, d) { return n >= 0 ? Math.floor(n / d) : -Math.floor(-n / d); }
function _hu(n, d) { // round n/d half up (away from zero for negatives), to an integer
  var s = n < 0 ? -1 : 1, a = Math.abs(n);
  return s * Math.floor((2 * a + d) / (2 * d));
}
function _dec(v, places) { // integer scaled by 10^places to text, trailing zeros dropped
  var neg = v < 0, a = Math.abs(v), base = Math.pow(10, places);
  var s = String(Math.floor(a / base)), f = String(a % base).padStart(places, "0").replace(/0+$/, "");
  return (neg ? "-" : "") + (f ? s + "." + f : s);
}
var _MIN = "the smallest size must be a whole number of px from 1 to 200";
var _MAX = "the largest size must be a whole number of px from 1 to 200";
var _W1 = "the smallest width must be a whole number of px from 200 to 4000";
var _W2 = "the largest width must be a whole number of px from 200 to 4000";
var _ROOT = "the root size must be a whole number of px from 8 to 32";
function _pair(a, b, c, d) {
  var m = _int(a, _MIN, 1, 200), M = _int(b, _MAX, 1, 200), w = _int(c, _W1, 200, 4000), W = _int(d, _W2, 200, 4000);
  if (M <= m) throw new Error("the largest size must be bigger than the smallest size");
  if (W <= w) throw new Error("the largest width must be wider than the smallest width");
  return [m, M, w, W];
}

function formulaTruth(minPx, maxPx, minW, maxW, rootPx) {
  var p = _pair(minPx, maxPx, minW, maxW), m = p[0], M = p[1], w = p[2], W = p[3];
  var r = _int(rootPx, _ROOT, 8, 32);
  var slope = _hu((M - m) * 100 * 10000, W - w);                          // vw, 4 places
  var icpt = _hu((m * (W - w) - (M - m) * w) * 10000, (W - w) * r);       // rem, 4 places
  var lo = _hu(m * 10000, r), hi = _hu(M * 10000, r);
  return "clamp(" + _dec(lo, 4) + "rem, " + _dec(icpt, 4) + "rem + " + _dec(slope, 4) + "vw, " + _dec(hi, 4) + "rem) takes the text from " + m + "px at " + w + "px wide to " + M + "px at " + W + "px wide, counting 1rem as " + r + "px. The numbers are rounded to 4 places, so the ends can be off by a tiny fraction of a pixel.";
}
function sizeTruth(minPx, maxPx, minW, maxW, atW) {
  var p = _pair(minPx, maxPx, minW, maxW), m = p[0], M = p[1], w = p[2], W = p[3];
  var v = _int(atW, "the viewport width must be a whole number of px from 1 to 20000", 1, 20000);
  if (v <= w) return "At " + v + "px wide the text sits at its smallest size, " + m + "px.";
  if (v >= W) return "At " + v + "px wide the text sits at its largest size, " + M + "px.";
  var s = _hu(((m * (W - w)) + (M - m) * (v - w)) * 100, W - w);
  return "At " + v + "px wide the text is " + _dec(s, 2) + "px, between " + m + "px and " + M + "px.";
}
function reachTruth(minPx, maxPx, minW, maxW, targetPx) {
  var p = _pair(minPx, maxPx, minW, maxW), m = p[0], M = p[1], w = p[2], W = p[3];
  var t = _int(targetPx, "the target size must be a whole number of px from 1 to 200", 1, 200);
  if (t < m || t > M) return "A size of " + t + "px is outside the range from " + m + "px to " + M + "px, so the text never has it.";
  var x = _hu((w * (M - m) + (t - m) * (W - w)) * 10, M - m);
  return "The text is " + t + "px at " + _dec(x, 1) + "px wide.";
}
