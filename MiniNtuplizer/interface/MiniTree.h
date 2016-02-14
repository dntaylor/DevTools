#ifndef MiniTree_h
#define MiniTree_h

#include <regex>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "TTree.h"

#include "FWCore/Utilities/interface/InputTag.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "CommonTools/Utils/interface/StringObjectFunction.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "DataFormats/PatCandidates/interface/PackedTriggerPrescales.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"

#include "DataFormats/Math/interface/deltaR.h"

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

    void AddCollectionToTree(std::string coll, std::string name, edm::ParameterSet pset);
    size_t GetTriggerBit(std::string trigName, const edm::TriggerNames& names);

    template<typename ObjType>
    bool MatchedToTriggerObject(ObjType obj, std::string trigName, const edm::TriggerNames& names);

    template<typename T, typename ObjType>
    T Evaluate(std::string branchName, std::string function, ObjType obj);

    template<typename ObjType>
    void AnalyzeCollection(edm::Handle<std::vector<ObjType> > objects, std::string name, const edm::TriggerNames& names);

    // tokens
    edm::EDGetTokenT<LHEEventProduct> lheEventProductToken_;
    edm::EDGetTokenT<GenEventInfoProduct> genEventInfoToken_;
    edm::EDGetTokenT<double> rhoToken_;
    edm::EDGetTokenT<std::vector<PileupSummaryInfo> > pileupSummaryInfoToken_;
    edm::EDGetTokenT<edm::TriggerResults> triggerBitsToken_;
    edm::EDGetTokenT<edm::TriggerResults> filterBitsToken_;
    edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> triggerObjectsToken_;
    edm::EDGetTokenT<pat::PackedTriggerPrescales> triggerPrescalesToken_;
    edm::EDGetTokenT<reco::VertexCollection> verticesToken_;
    edm::EDGetTokenT<reco::GenParticleCollection> genParticlesToken_;
    edm::EDGetTokenT<pat::ElectronCollection> electronsToken_;
    edm::EDGetTokenT<pat::MuonCollection> muonsToken_;
    edm::EDGetTokenT<pat::TauCollection> tausToken_;
    edm::EDGetTokenT<pat::PhotonCollection> photonsToken_;
    edm::EDGetTokenT<pat::JetCollection> jetsToken_;
    edm::EDGetTokenT<pat::METCollection> metsToken_;

    // handles
    edm::Handle<edm::TriggerResults> triggerBits_;
    edm::Handle<edm::TriggerResults> filterBits_;
    edm::Handle<pat::TriggerObjectStandAloneCollection> triggerObjects_;
    edm::Handle<pat::PackedTriggerPrescales> triggerPrescales_;

    // branch parameters
    edm::ParameterSet triggerBranches_;
    edm::ParameterSet filterBranches_;
    edm::ParameterSet vertexBranches_;
    edm::ParameterSet genParticleBranches_;
    edm::ParameterSet electronBranches_;
    edm::ParameterSet muonBranches_;
    edm::ParameterSet tauBranches_;
    edm::ParameterSet photonBranches_;
    edm::ParameterSet jetBranches_;
    edm::ParameterSet metBranches_;

    // other configurations
    bool isData_;

    // tree
    TTree *tree;
    TTree *lumitree;

    // lumitree branches
    Int_t   runBranch_;
    Int_t   lumiBranch_;
    Int_t   neventsBranch_;
    Float_t summedWeightsBranch_;

    // one off tree branches
    Int_t     isDataBranch_;
    Float_t   genWeightBranch_;
    ULong64_t eventBranch_;
    Float_t   rhoBranch_;
    Float_t   nTrueVerticesBranch_;
    Int_t     nupBranch_;

    // maps for branches
    std::map<std::string, UInt_t>                countMap_;
    std::map<std::string, std::vector<Float_t> > floatMap_;
    std::map<std::string, std::vector<Int_t> >   intMap_;

    // trigger
    std::vector<std::string>                 triggerNames_;
    std::vector<std::string>                 filterNames_;
    std::vector<std::string>                 triggerBranchStrings_;
    std::map<std::string, std::string>       triggerNamingMap_;
    std::map<std::string, std::vector<int> > triggerMatchMap_;
    std::map<std::string, Int_t>             triggerIntMap_;

    // collections
    std::vector<std::string> collectionOrder_;
    std::map<std::string, std::vector<std::string> > collectionNamesMap_;
    std::map<std::string, edm::ParameterSet> collectionPSetMap_;
    std::map<std::string, unsigned int> collectionMaxCounts_;
    std::map<std::string, std::string> collectionSelections_;
    std::map<std::string, std::vector<std::string> > collectionBranches_;
    std::map<std::string, std::string> branchTypes_;
    std::map<std::string, std::string> branchFunctions_;

};

void MiniTree::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}


DEFINE_FWK_MODULE(MiniTree);

#endif
