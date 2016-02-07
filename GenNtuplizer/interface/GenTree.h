#ifndef GenTree_h
#define GenTree_h

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

#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "DataFormats/JetReco/interface/GenJet.h"

class GenTree : public edm::one::EDAnalyzer<edm::one::SharedResources> {
  public:
    explicit GenTree(const edm::ParameterSet&);
    ~GenTree();

    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

  private:
    virtual void beginJob() override;
    virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
    virtual void endJob() override;

    void AddCollectionToTree(std::string name, edm::ParameterSet pset);

    template<typename T, typename ObjType>
    T Evaluate(std::string branchName, std::string function, ObjType obj);

    template<typename ObjType>
    void AnalyzeCollection(edm::Handle<std::vector<ObjType> > objects, std::string name);

    // tokens
    edm::EDGetTokenT<reco::GenParticleCollection> genParticlesToken_;
    edm::EDGetTokenT<reco::GenParticleCollection> higgsToken_;
    edm::EDGetTokenT<reco::GenParticleCollection> muonsToken_;
    edm::EDGetTokenT<reco::GenParticleCollection> electronsToken_;
    edm::EDGetTokenT<reco::GenParticleCollection> photonsToken_;
    edm::EDGetTokenT<reco::GenJetCollection> tausToken_;

    // branch parameters
    edm::ParameterSet genParticleBranches_;
    edm::ParameterSet higgsBranches_;
    edm::ParameterSet muonBranches_;
    edm::ParameterSet electronBranches_;
    edm::ParameterSet photonBranches_;
    edm::ParameterSet tauBranches_;

    // tree
    TTree *tree;

    // maps for branches
    std::map<std::string, UInt_t>                countMap_;
    std::map<std::string, std::vector<Float_t> > floatMap_;
    std::map<std::string, std::vector<Int_t> >   intMap_;

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

void GenTree::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}


DEFINE_FWK_MODULE(GenTree);

#endif
