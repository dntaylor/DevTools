#include "AnalysisTools/GenNtuplizer/interface/GenTree.h"

GenTree::GenTree(const edm::ParameterSet &iConfig) :
    genParticlesToken_(consumes<reco::GenParticleCollection>(iConfig.getParameter<edm::InputTag>("genParticles"))),
    higgsToken_(consumes<reco::GenParticleCollection>(iConfig.getParameter<edm::InputTag>("higgs"))),
    muonsToken_(consumes<reco::GenParticleCollection>(iConfig.getParameter<edm::InputTag>("muons"))),
    electronsToken_(consumes<reco::GenParticleCollection>(iConfig.getParameter<edm::InputTag>("electrons"))),
    photonsToken_(consumes<reco::GenParticleCollection>(iConfig.getParameter<edm::InputTag>("photons"))),
    tausToken_(consumes<reco::GenJetCollection>(iConfig.getParameter<edm::InputTag>("taus"))),
    genParticleBranches_(iConfig.getParameter<edm::ParameterSet>("genParticleBranches")),
    higgsBranches_(iConfig.getParameter<edm::ParameterSet>("higgsBranches")),
    muonBranches_(iConfig.getParameter<edm::ParameterSet>("muonBranches")),
    electronBranches_(iConfig.getParameter<edm::ParameterSet>("electronBranches")),
    photonBranches_(iConfig.getParameter<edm::ParameterSet>("photonBranches")),
    tauBranches_(iConfig.getParameter<edm::ParameterSet>("tauBranches"))
{
    // Declare use of TFileService
    usesResource("TFileService");
    // retrieve parameters
    collectionNamesMap_.insert(std::pair<std::string, std::vector<std::string> >("genParticles",genParticleBranches_.getParameterNames()));
    collectionNamesMap_.insert(std::pair<std::string, std::vector<std::string> >("higgs",higgsBranches_.getParameterNames()));
    collectionNamesMap_.insert(std::pair<std::string, std::vector<std::string> >("muons",muonBranches_.getParameterNames()));
    collectionNamesMap_.insert(std::pair<std::string, std::vector<std::string> >("electrons",electronBranches_.getParameterNames()));
    collectionNamesMap_.insert(std::pair<std::string, std::vector<std::string> >("photons",photonBranches_.getParameterNames()));
    collectionNamesMap_.insert(std::pair<std::string, std::vector<std::string> >("taus",tauBranches_.getParameterNames()));
    collectionPSetMap_.insert(std::pair<std::string, edm::ParameterSet>("genParticles",genParticleBranches_));
    collectionPSetMap_.insert(std::pair<std::string, edm::ParameterSet>("higgs",higgsBranches_));
    collectionPSetMap_.insert(std::pair<std::string, edm::ParameterSet>("muons",muonBranches_));
    collectionPSetMap_.insert(std::pair<std::string, edm::ParameterSet>("electrons",electronBranches_));
    collectionPSetMap_.insert(std::pair<std::string, edm::ParameterSet>("photons",photonBranches_));
    collectionPSetMap_.insert(std::pair<std::string, edm::ParameterSet>("taus",tauBranches_));
    // order for tree
    collectionOrder_.push_back("genParticles");
    collectionOrder_.push_back("higgs");
    collectionOrder_.push_back("electrons");
    collectionOrder_.push_back("muons");
    collectionOrder_.push_back("photons");
    collectionOrder_.push_back("taus");
    // Check for duplicate entries
    std::set<std::string> allBranches;
    for (auto coll : collectionOrder_) {
        for (auto collectionName : collectionNamesMap_[coll]) {
            // first the counter
            std::string countName = collectionName + "_count";
            if (allBranches.count(countName)) {
                throw cms::Exception("DuplicatedBranch")
                    << "Branch name \"" << countName <<"\" already added to ntuple." << std::endl;
            }
            allBranches.insert(countName);
            // now all branches
            edm::ParameterSet collection = collectionPSetMap_[coll].getParameter<edm::ParameterSet>(collectionName);
            edm::ParameterSet collectionBranches = collection.getParameter<edm::ParameterSet>("branches");
            std::vector<std::string> branchNames = collectionBranches.getParameterNames();
            for (auto branchName : branchNames) {
                std::string name = collectionName + '_' + branchName;
                if (allBranches.count(name)) {
                    throw cms::Exception("DuplicatedBranch")
                        << "Branch name \"" << name <<"\" already added to ntuple." << std::endl;
                }
                allBranches.insert(name);
            }
        }
    }
}

GenTree::~GenTree() { }

void GenTree::AddCollectionToTree(std::string name, edm::ParameterSet pset) {
    // Add the count
    std::string countName = name + "_count";
    countMap_.insert(std::pair<std::string, UInt_t>(name, 0));
    std::string leafString = countName + "/i";
    tree->Branch(countName.c_str(),&countMap_[name],leafString.c_str());
    // Add the rest of the branches
    edm::ParameterSet collectionBranches = pset.getParameter<edm::ParameterSet>("branches");
    unsigned int maxCount = pset.getParameter<unsigned int>("maxCount");
    collectionMaxCounts_.insert(std::pair<std::string, unsigned int>(name, maxCount));
    std::string selection = pset.exists("selection") ? pset.getParameter<std::string>("selection") : "";
    collectionSelections_.insert(std::pair<std::string, std::string>(name, selection));
    std::vector<std::string> branchNames = collectionBranches.getParameterNames();
    std::vector<std::string> treeBranchNames;
    for (auto branchName : branchNames) {
        std::string treeBranchName = name + "_" + branchName;
        treeBranchNames.push_back(treeBranchName);
        std::vector<std::string> branchParams = collectionBranches.getParameter<std::vector<std::string>>(branchName);
        branchTypes_.insert(std::pair<std::string, std::string>(treeBranchName, branchParams[1]));
        branchFunctions_.insert(std::pair<std::string, std::string>(treeBranchName, branchParams[0]));
        std::string branchLeafString = treeBranchName + "[" + countName + "]/" + branchParams[1];
        if (branchParams[1]=="F") { // Float_t
            std::vector<Float_t> branch(maxCount);
            floatMap_.insert(std::pair<std::string, std::vector<Float_t> >(treeBranchName,branch));
            tree->Branch(treeBranchName.c_str(), &floatMap_[treeBranchName]);
        }
        else if (branchParams[1]=="I") { // Int_t
            std::vector<Int_t> branch(maxCount);
            intMap_.insert(std::pair<std::string, std::vector<Int_t>>(treeBranchName,branch));
            tree->Branch(treeBranchName.c_str(), &intMap_[treeBranchName]);
        }
        else {
            throw cms::Exception("UnrecognizedType")
                << "Unknown type \"" << branchParams[1] <<"\" for branch \"" <<  treeBranchName << "\"." << std::endl;
        }
    }
    collectionBranches_.insert(std::pair<std::string, std::vector<std::string> >(name, treeBranchNames));
}

void GenTree::beginJob() {
    edm::Service<TFileService> FS;
    tree = FS->make<TTree>("GenTree", "GenTree");

    // create branches
    for (auto coll : collectionOrder_) {
        for (auto collectionName : collectionNamesMap_[coll]) {
            edm::ParameterSet collectionPSet = collectionPSetMap_[coll].getParameter<edm::ParameterSet>(collectionName);
            GenTree::AddCollectionToTree(collectionName,collectionPSet);
        }
    }

}

void GenTree::endJob() { }

template<typename T, typename ObjType>
T GenTree::Evaluate(std::string branchName, std::string function, ObjType obj) {
    StringObjectFunction<ObjType> func_(function,true);
    T val;
    try{
        val = func_(obj);
    } catch(cms::Exception& iException) {
        iException << "Caught exception in evaluating branch "
            << branchName << " with formula: " << function << ".";
        throw;
    }
    return val;
}

template<typename ObjType>
void GenTree::AnalyzeCollection(edm::Handle<std::vector<ObjType> > objects, std::string name) {

    // cleanup from before
    for (auto collectionName: collectionNamesMap_[name]) {
        countMap_[collectionName] = 0;
        for (auto branchName : collectionBranches_[collectionName]) {
            std::string branchType = branchTypes_[branchName];
            if (branchType=="F") { // Float_t
                floatMap_[branchName].clear();
            }
            else if (branchType=="I") { // Int_t
                intMap_[branchName].clear();
            }
            else {
                throw cms::Exception("UnrecognizedType")
                    << "Unknown type \"" << branchType <<"\" for branch \"" <<  branchName << "\"." << std::endl;
            }
        }
    }
    // iterate over all particles
    for ( auto& object : *objects ) {
        // iterate over collections
        for (auto collectionName : collectionNamesMap_[name]) {
            std::string countName = collectionName + "_count";
            UInt_t counter = countMap_[collectionName];
            unsigned int maxCount = collectionMaxCounts_[collectionName];
            // see if we want to store the collection
            if (collectionSelections_[collectionName]!="") {
                StringCutObjectSelector<ObjType> selector(collectionSelections_[collectionName]);
                if (!selector(object)) {
                    continue;
                }
            }
            // See if we are past max counts
            if (counter >= maxCount) {
                if (counter == maxCount) {
                    std::cout << "Warning: " << collectionName << " has more objects than max count of " << maxCount << "." << std::endl;
                    std::cout << "The rest will be skipped." << std::endl;
                }
                countMap_[collectionName]++;
                continue;
            }
            // iterate through each branch
            for (auto branchName : collectionBranches_[collectionName]) {
                std::string function = branchFunctions_[branchName];
                std::string branchType = branchTypes_[branchName];
                if (branchType=="F") { // Float_t
                    floatMap_[branchName].push_back(GenTree::Evaluate<Float_t,ObjType>(branchName,function,object));
                }
                else if (branchType=="I") { // Int_t
                    intMap_[branchName].push_back(GenTree::Evaluate<Int_t,ObjType>(branchName,function,object));
                }
                else {
                    throw cms::Exception("UnrecognizedType")
                        << "Unknown type \"" << branchType <<"\" for branch \"" <<  branchName << "\"." << std::endl;
                }
            }
            countMap_[collectionName]++;
        }
    }

}


void GenTree::analyze(const edm::Event &iEvent, const edm::EventSetup &iSetup) {

    edm::Handle<reco::GenParticleCollection> genParticles;
    iEvent.getByToken(genParticlesToken_, genParticles);

    edm::Handle<reco::GenParticleCollection> higgs;
    iEvent.getByToken(higgsToken_, higgs);

    edm::Handle<reco::GenParticleCollection> muons;
    iEvent.getByToken(muonsToken_, muons);

    edm::Handle<reco::GenParticleCollection> electrons;
    iEvent.getByToken(electronsToken_, electrons);

    edm::Handle<reco::GenParticleCollection> photons;
    iEvent.getByToken(photonsToken_, photons);

    edm::Handle<reco::GenJetCollection> taus;
    iEvent.getByToken(tausToken_, taus);

    GenTree::AnalyzeCollection<reco::GenParticle>(genParticles,"genParticles");
    GenTree::AnalyzeCollection<reco::GenParticle>(higgs,"higgs");
    GenTree::AnalyzeCollection<reco::GenParticle>(muons,"muons");
    GenTree::AnalyzeCollection<reco::GenParticle>(electrons,"electrons");
    GenTree::AnalyzeCollection<reco::GenParticle>(photons,"photons");
    GenTree::AnalyzeCollection<reco::GenJet>(taus,"taus");

    tree->Fill();
}
