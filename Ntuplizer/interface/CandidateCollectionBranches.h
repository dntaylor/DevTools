#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Framework/interface/Event.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "CommonTools/Utils/interface/StringObjectFunction.h"
#include "DataFormats/Candidate/interface/Candidate.h"

#include "TTree.h"

template<typename T>
class CandidateCollectionFunction {
  public:
    CandidateCollectionFunction(TTree * tree, std::string functionName, std::string functionString);
    void evaluate(const reco::CandidateView& candidates);

  private:
    StringObjectFunction<reco::Candidate, true> function_;
    TBranch * vectorBranch_;
    std::vector<T> values_;
};

typedef CandidateCollectionFunction<int> CandidateCollectionIntFunction;
typedef CandidateCollectionFunction<float> CandidateCollectionFloatFunction;

class CandidateCollectionBranches {
  public:
    CandidateCollectionBranches(TTree * tree, std::string collectionName,  const edm::ParameterSet& iConfig, edm::ConsumesCollector cc);
    void fill(const edm::Event& iEvent);
    std::string getName() { return collectionName_; }
    int getCount() { return collectionCount_; }

  private:
    edm::EDGetTokenT<reco::CandidateView> collectionToken_;
    edm::ParameterSet branches_;
    std::vector<std::unique_ptr<CandidateCollectionFloatFunction> > floatFunctions_;
    std::vector<std::unique_ptr<CandidateCollectionIntFunction> > intFunctions_;
    TBranch * collectionCountBranch_;
    std::string collectionName_;
    int collectionCount_;
};
