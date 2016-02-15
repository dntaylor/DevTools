#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Framework/interface/Event.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "CommonTools/Utils/interface/StringObjectFunction.h"
#include "DataFormats/Candidate/interface/Candidate.h"

#include "TTree.h"

template<typename T>
class CollectionFunction {
  public:
    CollectionFunction(TTree * tree, std::string functionName, std::string functionString);
    void evaluate(const reco::CandidateView& candidates);

  private:
    StringObjectFunction<reco::Candidate, true> function_;
    TBranch * vectorBranch_;
    std::vector<T> values_;
};

typedef CollectionFunction<int> CollectionIntFunction;
typedef CollectionFunction<float> CollectionFloatFunction;

class CandidateCollectionBranches {
  public:
    CandidateCollectionBranches(TTree * tree, std::string collectionName,  const edm::ParameterSet& iConfig, edm::ConsumesCollector cc);
    void fill(const edm::Event& iEvent);

  private:
    edm::EDGetTokenT<reco::CandidateView> collectionToken_;
    edm::ParameterSet branches_;
    std::vector<std::unique_ptr<CollectionFloatFunction> > floatFunctions_;
    std::vector<std::unique_ptr<CollectionIntFunction> > intFunctions_;
    TBranch * collectionCountBranch_;
    int collectionCount_;
};
