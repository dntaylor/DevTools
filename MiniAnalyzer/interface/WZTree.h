#ifndef WZTree_h
#define WZTree_h

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "TTree.h"
#include "TChain.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"


class WZTree : public edm::one::EDAnalyzer<edm::one::SharedResources> {
  public:
    explicit WZTree(const edm::ParameterSet&);
    ~WZTree();

    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

  private:
    virtual void beginJob() override;
    virtual void analyze(edm::Event const& iEvent, edm::EventSetup const&) override;
    virtual void endJob() override;

    // tchain
    TChain* inputTree_;
    TChain* inputLumi_;

    // tree
    TTree* tree_;

    // parameters
    std::vector<std::string> inputFileNames_;
    std::string              inputTreeName_;
    std::string              inputLumiName_;
    std::string              inputDirectoryName_;
    std::string              treeName_;
};

void WZTree::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}


DEFINE_FWK_MODULE(WZTree);

#endif
