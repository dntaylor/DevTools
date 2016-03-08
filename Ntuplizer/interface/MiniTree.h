#ifndef MiniTree_h
#define MiniTree_h

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
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "DataFormats/PatCandidates/interface/PackedTriggerPrescales.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

#include "DataFormats/Math/interface/deltaR.h"

#include "DevTools/Ntuplizer/interface/CandidateCollectionBranches.h"
#include "DevTools/Ntuplizer/interface/VertexCollectionBranches.h"

class MiniTree : public edm::one::EDAnalyzer<edm::one::SharedResources,edm::one::WatchLuminosityBlocks> {
  public:
    explicit MiniTree(const edm::ParameterSet&);
    ~MiniTree();

    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

  private:
    virtual void beginJob() override;
    virtual void beginLuminosityBlock(edm::LuminosityBlock const& iEvent, edm::EventSetup const&) override;
    virtual void analyze(edm::Event const& iEvent, edm::EventSetup const&) override;
    virtual void endLuminosityBlock(edm::LuminosityBlock const& iEvent, edm::EventSetup const&) override;
    virtual void endJob() override;

    size_t GetTriggerBit(std::string trigName, const edm::TriggerNames& names);

    // tokens
    edm::EDGetTokenT<LHEEventProduct> lheEventProductToken_;
    edm::EDGetTokenT<GenEventInfoProduct> genEventInfoToken_;
    edm::EDGetTokenT<double> rhoToken_;
    edm::EDGetTokenT<std::vector<PileupSummaryInfo> > pileupSummaryInfoToken_;
    edm::EDGetTokenT<edm::TriggerResults> triggerBitsToken_;
    edm::EDGetTokenT<edm::TriggerResults> filterBitsToken_;
    edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> triggerObjectsToken_;
    edm::EDGetTokenT<pat::PackedTriggerPrescales> triggerPrescalesToken_;

    // handles
    edm::Handle<edm::TriggerResults> triggerBits_;
    edm::Handle<edm::TriggerResults> filterBits_;
    edm::Handle<pat::TriggerObjectStandAloneCollection> triggerObjects_;
    edm::Handle<pat::PackedTriggerPrescales> triggerPrescales_;

    // branch parameters
    edm::ParameterSet triggerBranches_;
    edm::ParameterSet filterBranches_;

    edm::ParameterSet collections_;
    edm::ParameterSet vertexCollections_;

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
    Int_t                 isDataBranch_;
    Float_t               genWeightBranch_;
    Int_t                 numWeightsBranch_;
    std::vector<Float_t>  genWeightsBranch_;
    ULong64_t             eventBranch_;
    Float_t               rhoBranch_;
    Float_t               nTrueVerticesBranch_;
    Int_t                 nupBranch_;
    Int_t                 numGenJetsBranch_;
    Float_t               genHTBranch_;

    // trigger
    std::vector<std::string>                 triggerNames_;
    std::vector<std::string>                 filterNames_;
    std::vector<std::string>                 triggerBranchStrings_;
    std::map<std::string, std::string>       triggerNamingMap_;
    std::map<std::string, Int_t>             triggerIntMap_;

    // collections
    std::vector<std::unique_ptr<CandidateCollectionBranches> > collectionBranches_;
    std::vector<std::unique_ptr<VertexCollectionBranches> > vertexCollectionBranches_;
};

void MiniTree::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}


DEFINE_FWK_MODULE(MiniTree);

#endif
