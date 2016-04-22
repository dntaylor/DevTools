#ifndef GenMiniTree_h
#define GenMiniTree_h

#include <regex>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "TTree.h"

#include "FWCore/Utilities/interface/InputTag.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "CommonTools/Utils/interface/StringObjectFunction.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

#include "DataFormats/Math/interface/deltaR.h"

#include "DevTools/Ntuplizer/interface/CandidateCollectionBranches.h"

class GenMiniTree : public edm::one::EDAnalyzer<edm::one::SharedResources,edm::one::WatchLuminosityBlocks> {
  public:
    explicit GenMiniTree(const edm::ParameterSet&);
    ~GenMiniTree();

    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

  private:
    virtual void beginJob() override;
    virtual void beginLuminosityBlock(edm::LuminosityBlock const& iEvent, edm::EventSetup const&) override;
    virtual void analyze(edm::Event const& iEvent, edm::EventSetup const&) override;
    virtual void endLuminosityBlock(edm::LuminosityBlock const& iEvent, edm::EventSetup const&) override;
    virtual void endJob() override;

    // tokens
    edm::EDGetTokenT<LHEEventProduct> lheEventProductToken_;
    edm::EDGetTokenT<GenEventInfoProduct> genEventInfoToken_;
    edm::EDGetTokenT<std::vector<PileupSummaryInfo> > pileupSummaryInfoToken_;

    // branch parameters
    edm::ParameterSet collections_;

    // other configurations
    bool isData_;

    // tree
    TTree *tree_;
    TTree *lumitree_;

    // lumitree branches
    Int_t   runBranch_;
    Int_t   lumiBranch_;
    Int_t   neventsBranch_;
    Float_t summedWeightsBranch_;

    // one off tree branches
    Float_t               genWeightBranch_;
    Int_t                 numWeightsBranch_;
    std::vector<Float_t>  genWeightsBranch_;
    ULong64_t             eventBranch_;
    Float_t               nTrueVerticesBranch_;
    Int_t                 nupBranch_;
    Int_t                 numGenJetsBranch_;
    Float_t               genHTBranch_;

    // collections
    std::vector<std::unique_ptr<CandidateCollectionBranches> > collectionBranches_;
};

void GenMiniTree::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}


DEFINE_FWK_MODULE(GenMiniTree);

#endif

