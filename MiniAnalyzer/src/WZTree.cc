#include "AnalysisTools/MiniAnalyzer/interface/WZTree.h"

WZTree::WZTree(const edm::ParameterSet &iConfig) :
    inputFileNames_(iConfig.getParameter<std::vector<std::string> >("fileNames")),
    inputTreeName_(iConfig.getParameter<std::string>("inputTreeName")),
    inputLumiName_(iConfig.getParameter<std::string>("inputLumiName")),
    inputDirectoryName_(iConfig.getParameter<std::string>("inputDirectoryName")),
    treeName_(iConfig.getParameter<std::string>("outputTreeName"))
{
    // Declare use of TFileService
    usesResource("TFileService");

    // get the tchain
    inputTree_ = new TChain((inputDirectoryName_+"/"+inputTreeName_).c_str());
    inputLumi_ = new TChain((inputDirectoryName_+"/"+inputLumiName_).c_str());
    for (size_t i=0; i<inputFileNames_.size(); i++) {
        inputTree_->Add(inputFileNames_[i].c_str());
        inputLumi_->Add(inputFileNames_[i].c_str());
    }

    // make the tree
    edm::Service<TFileService> FS;

    tree_ = FS->make<TTree>(treeName_.c_str(), treeName_.c_str());
}

WZTree::~WZTree() { }

void WZTree::beginJob() { }

void WZTree::endJob() { }

void WZTree::analyze(const edm::Event &iEvent, const edm::EventSetup &iSetup) { }
