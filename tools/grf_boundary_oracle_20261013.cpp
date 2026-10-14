// Project-owned deterministic arithmetic oracle. This does not link to grf.
#include <cmath>
#include <iomanip>
#include <iostream>
#include <map>
#include <numeric>
#include <stdexcept>
#include <vector>

using V = std::vector<double>;

double average(const V& score, const V& weight) {
  if (score.empty() || score.size() != weight.size()) throw std::invalid_argument("shape");
  double value = 0, mass = 0;
  for (std::size_t i = 0; i < score.size(); ++i) {
    if (!std::isfinite(score[i]) || !std::isfinite(weight[i]) || weight[i] < 0)
      throw std::invalid_argument("nonfinite_or_negative_weight");
    value += score[i]*weight[i]; mass += weight[i];
  }
  if (!(mass > 0)) throw std::invalid_argument("zero_mass");
  return value/mass;
}

double group_variance(const V& score, const V& weight, const std::vector<int>& cluster) {
  const double target = average(score, weight);
  if (cluster.size() != score.size()) throw std::invalid_argument("cluster_shape");
  std::map<int, double> total, mass;
  for (std::size_t i = 0; i < score.size(); ++i) {
    total[cluster[i]] += weight[i]*(score[i]-target);
    mass[cluster[i]] += weight[i];
  }
  double ss = 0, all_mass = 0, groups = 0;
  for (const auto& item : mass) {
    all_mass += item.second;
    if (item.second > 0) { ++groups; ss += total[item.first]*total[item.first]; }
  }
  if (groups <= 1) throw std::invalid_argument("one_positive_weight_cluster");
  return ss/(all_mass*all_mass)*groups/(groups-1);
}

double aipw(double y, int treatment, double m, double e, double tau) {
  if ((treatment != 0 && treatment != 1) || !std::isfinite(e) || e <= 0 || e >= 1)
    throw std::invalid_argument("unsupported_treatment_or_propensity");
  if (!std::isfinite(y) || !std::isfinite(m) || !std::isfinite(tau))
    throw std::invalid_argument("nonfinite_nuisance_or_outcome");
  return tau+(treatment-e)/(e*(1-e))*(y-m-tau*(treatment-e));
}

double local_slope(const V& y, const V& treatment, const V& weight) {
  const double my = average(y, weight), mw = average(treatment, weight);
  double cov = 0, var = 0;
  for (std::size_t i = 0; i < y.size(); ++i) {
    cov += weight[i]*(y[i]-my)*(treatment[i]-mw);
    var += weight[i]*(treatment[i]-mw)*(treatment[i]-mw);
  }
  const double mass = std::accumulate(weight.begin(), weight.end(), 0.0);
  if (var/mass <= 1e-12) throw std::invalid_argument("weak_local_treatment_variation");
  return cov/var;
}

template<class Fn> int rejects(Fn fn) {
  try { fn(); } catch (const std::invalid_argument&) { return 1; }
  throw std::runtime_error("Expected rejection was not observed");
}

int main() {
  const V s{10,10,40,40,40,40}, unit(6,1), equal{.5,.5,.25,.25,.25,.25};
  const std::vector<int> clusters{0,0,1,1,1,1}, rows{0,1,2,3,4,5};
  const V scores{aipw(0,0,1,.25,2),aipw(1,0,1,.5,2),
                 aipw(3,1,2,.5,2),aipw(5,1,2,.75,2)};
  const V column_major{1,2,3,10,20,30}, mistaken_row_major{1,10,2,20,3,30};
  const auto at = [](const V& x, std::size_t row, std::size_t col) {return x.at(col*3+row);};
  int refused = 0;
  refused += rejects([&](){return average(s,V(6,0));});
  refused += rejects([&](){return group_variance(s,unit,std::vector<int>(6,0));});
  refused += rejects([&](){return aipw(1,1,0,0,1);});
  refused += rejects([&](){return average(s,V(6,-1));});
  refused += rejects([&](){return local_slope(V{1,2,3,4},V(4,.5),V(4,1));});
  std::cout << std::setprecision(17)
    << "{\"kind\":\"project_cpp_arithmetic_not_grf_execution\","
    << "\"person_mean\":" << average(s,unit) << ','
    << "\"cluster_mean\":" << average(s,equal) << ','
    << "\"iid_variance\":" << group_variance(s,unit,rows) << ','
    << "\"cluster_variance\":" << group_variance(s,unit,clusters) << ','
    << "\"equal_cluster_variance\":" << group_variance(s,equal,clusters) << ','
    << "\"aipw_mean\":" << average(scores,V(4,1)) << ','
    << "\"local_slope\":" << local_slope(V{-2,-1,1,2},V{-.5,-.5,.5,.5},V(4,1)) << ','
    << "\"column_major_value\":" << at(column_major,1,1) << ','
    << "\"wrong_row_major_value\":" << at(mistaken_row_major,1,1) << ','
    << "\"rejections\":" << refused << "}\n";
}
