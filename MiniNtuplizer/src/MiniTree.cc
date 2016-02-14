#include "AnalysisTools/MiniNtuplizer/interface/MiniTree.h"

MiniTree::MiniTree(const edm::ParameterSet &iConfig) :
    lheEventProductToken_(consumes<LHEEventProduct>(iConfig.getParameter<edm::InputTag>("lheEventProduct"))),
    genEventInfoToken_(consumes<GenEventInfoProduct>(iConfig.getParameter<edm::InputTag>("genEventInfo"))),
    rhoToken_(consumes<double>(iConfig.getParameter<edm::InputTag>("rho"))),
    pileupSummaryInfoToken_(consumes<std::vector<PileupSummaryInfo> >(iConfig.getParameter<edm::InputTag>("pileupSummaryInfo"))),
    triggerBitsToken_(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("triggerResults"))),
    triggerObjectsToken_(consumes<pat::TriggerObjectStandAloneCollection>(iConfig.getParameter<edm::InputTag>("triggerObjects"))),
    triggerPrescalesToken_(consumes<pat::PackedTriggerPrescales>(iConfig.getParameter<edm::InputTag>("triggerPrescales"))),
    verticesToken_(consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vertices"))),
    genParticlesToken_(consumes<reco::GenParticleCollection>(iConfig.getParameter<edm::InputTag>("genParticles"))),
    electronsToken_(consumes<pat::ElectronCollection>(iConfig.getParameter<edm::InputTag>("electrons"))),
    muonsToken_(consumes<pat::MuonCollection>(iConfig.getParameter<edm::InputTag>("muons"))),
    tausToken_(consumes<pat::TauCollection>(iConfig.getParameter<edm::InputTag>("taus"))),
    photonsToken_(consumes<pat::PhotonCollection>(iConfig.getParameter<edm::InputTag>("photons"))),
    jetsToken_(consumes<pat::JetCollection>(iConfig.getParameter<edm::InputTag>("jets"))),
    metsToken_(consumes<pat::METCollection>(iConfig.getParameter<edm::InputTag>("mets"))),
    triggerBranches_(iConfig.getParameter<edm::ParameterSet>("triggerBranches")),
    vertexBranches_(iConfig.getParameter<edm::ParameterSet>("vertexBranches")),
    genParticleBranches_(iConfig.getParameter<edm::ParameterSet>("genParticleBranches")),
    electronBranches_(iConfig.getParameter<edm::ParameterSet>("electronBranches")),
    muonBranches_(iConfig.getParameter<edm::ParameterSet>("muonBranches")),
    tauBranches_(iConfig.getParameter<edm::ParameterSet>("tauBranches")),
    photonBranches_(iConfig.getParameter<edm::ParameterSet>("photonBranches")),
    jetBranches_(iConfig.getParameter<edm::ParameterSet>("jetBranches")),
    metBranches_(iConfig.getParameter<edm::ParameterSet>("metBranches")),
    isData_(iConfig.getParameter<bool>("isData"))
{
    // Declare use of TFileService
    usesResource("TFileService");
    // store names
    collectionNamesMap_.insert(std::pair<std::string, std::vector<std::string> >("vertices",vertexBranches_.getParameterNames()));
    collectionNamesMap_.insert(std::pair<std::string, std::vector<std::string> >("genParticles",genParticleBranches_.getParameterNames()));
    collectionNamesMap_.insert(std::pair<std::string, std::vector<std::string> >("electrons",electronBranches_.getParameterNames()));
    collectionNamesMap_.insert(std::pair<std::string, std::vector<std::string> >("muons",muonBranches_.getParameterNames()));
    collectionNamesMap_.insert(std::pair<std::string, std::vector<std::string> >("taus",tauBranches_.getParameterNames()));
    collectionNamesMap_.insert(std::pair<std::string, std::vector<std::string> >("photons",photonBranches_.getParameterNames()));
    collectionNamesMap_.insert(std::pair<std::string, std::vector<std::string> >("jets",jetBranches_.getParameterNames()));
    collectionNamesMap_.insert(std::pair<std::string, std::vector<std::string> >("mets",metBranches_.getParameterNames()));
    // store parameters
    collectionPSetMap_.insert(std::pair<std::string, edm::ParameterSet>("vertices",vertexBranches_));
    collectionPSetMap_.insert(std::pair<std::string, edm::ParameterSet>("genParticles",genParticleBranches_));
    collectionPSetMap_.insert(std::pair<std::string, edm::ParameterSet>("electrons",electronBranches_));
    collectionPSetMap_.insert(std::pair<std::string, edm::ParameterSet>("muons",muonBranches_));
    collectionPSetMap_.insert(std::pair<std::string, edm::ParameterSet>("taus",tauBranches_));
    collectionPSetMap_.insert(std::pair<std::string, edm::ParameterSet>("photons",photonBranches_));
    collectionPSetMap_.insert(std::pair<std::string, edm::ParameterSet>("jets",jetBranches_));
    collectionPSetMap_.insert(std::pair<std::string, edm::ParameterSet>("mets",metBranches_));
    // order for tree
    collectionOrder_.push_back("vertices");
    collectionOrder_.push_back("genParticles");
    collectionOrder_.push_back("electrons");
    collectionOrder_.push_back("muons");
    collectionOrder_.push_back("taus");
    collectionOrder_.push_back("photons");
    collectionOrder_.push_back("jets");
    collectionOrder_.push_back("mets");
    // Check for duplicate entries
    std::set<std::string> allBranches;
    // get trigger parameters
    triggerBranchStrings_.push_back("Pass");
    triggerBranchStrings_.push_back("Prescale");
    triggerNames_ = triggerBranches_.getParameterNames();
    for (auto trig : triggerNames_) {
        edm::ParameterSet trigPSet = triggerBranches_.getParameter<edm::ParameterSet>(trig);
        std::string trigString = trigPSet.getParameter<std::string>("path");
        std::vector<int> trigMatchPdgids = trigPSet.getParameter<std::vector<int> >("pdgid");
        triggerNamingMap_.insert(std::pair<std::string, std::string>(trig,trigString));
        triggerMatchMap_.insert(std::pair<std::string, std::vector<int> >(trig,trigMatchPdgids));
        for (auto branch : triggerBranchStrings_) {
            std::string branchName = trig + branch;
            if (allBranches.count(branchName)) {
                throw cms::Exception("DuplicatedBranch")
                    << "Branch name \"" << branchName <<"\" already added to ntuple." << std::endl;
            }
            allBranches.insert(branchName);
        }
    }
    // collection parameters
    for (auto coll : collectionOrder_) {
        for (auto collectionName : collectionNamesMap_[coll]) {
            // first the counter
            std::string countName = collectionName + "_count";
            if (allBranches.count(countName)) {
                throw cms::Exception("DuplicatedBranch")
                    << "Branch name \"" << countName <<"\" already added to ntuple." << std::endl;
            }
            allBranches.insert(countName);
            // trigger matching branches
            for (auto trig : triggerNames_) {
                for (auto pdgid : triggerMatchMap_[trig]) {
                    if ((pdgid==11 && coll=="electrons") ||
                        (pdgid==13 && coll=="muons") ||
                        (pdgid==15 && coll=="taus") ||
                        (pdgid==22 && coll=="photons")) {
                        std::string matchBranchName = collectionName + "_matches" + trig;
                        if (allBranches.count(matchBranchName)) {
                            throw cms::Exception("DuplicatedBranch")
                                << "Branch name \"" << matchBranchName <<"\" already added to ntuple." << std::endl;
                        }
                        allBranches.insert(matchBranchName);
                    }
                }
            }
            // now collection specific branches
            edm::ParameterSet collection = collectionPSetMap_[coll].getParameter<edm::ParameterSet>(collectionName);
            edm::ParameterSet collectionBranches = collection.getParameter<edm::ParameterSet>("branches");
            std::vector<std::string> branchNames = collectionBranches.getParameterNames();
            for (auto branchName : branchNames) {
                std::string name = collectionName + "_" + branchName;
                if (allBranches.count(name)) {
                    throw cms::Exception("DuplicatedBranch")
                        << "Branch name \"" << name <<"\" already added to ntuple." << std::endl;
                }
                allBranches.insert(name);
            }
        }
    }
}

MiniTree::~MiniTree() { }

void MiniTree::AddCollectionToTree(std::string coll, std::string name, edm::ParameterSet pset) {
    // Add the count
    std::string countName = name + "_count";
    countMap_.insert(std::pair<std::string, UInt_t>(name, 0));
    std::string leafString = countName + "/i";
    tree->Branch(countName.c_str(),&countMap_[name],leafString.c_str());
    // get branch params
    edm::ParameterSet collectionBranches = pset.getParameter<edm::ParameterSet>("branches");
    unsigned int maxCount = pset.getParameter<unsigned int>("maxCount");
    collectionMaxCounts_.insert(std::pair<std::string, unsigned int>(name, maxCount));
    std::string selection = pset.exists("selection") ? pset.getParameter<std::string>("selection") : "";
    collectionSelections_.insert(std::pair<std::string, std::string>(name, selection));
    // trigger matching
    for (std::string trig : triggerNames_) {
        for (int pdgid : triggerMatchMap_[trig]) {
            if ((pdgid==11 && coll=="electrons") ||
                (pdgid==13 && coll=="muons") ||
                (pdgid==15 && coll=="taus") ||
                (pdgid==22 && coll=="photons")) {
                std::string matchBranchName = name + "_matches_" + trig;
                std::vector<Int_t> branch(maxCount);
                intMap_.insert(std::pair<std::string, std::vector<Int_t> >(matchBranchName,branch));
                tree->Branch(matchBranchName.c_str(), &intMap_[matchBranchName]);
            }
        }
    }
    // Add the rest of the branches
    std::vector<std::string> branchNames = collectionBranches.getParameterNames();
    std::vector<std::string> treeBranchNames;
    for (auto branchName : branchNames) {
        std::string treeBranchName = name + "_" + branchName;
        treeBranchNames.push_back(treeBranchName);
        std::vector<std::string> branchParams = collectionBranches.getParameter<std::vector<std::string>>(branchName);
        branchTypes_.insert(std::pair<std::string, std::string>(treeBranchName, branchParams[1]));
        branchFunctions_.insert(std::pair<std::string, std::string>(treeBranchName, branchParams[0]));
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

void MiniTree::beginJob() {
    edm::Service<TFileService> FS;

    // create lumitree
    lumitree = FS->make<TTree>("LumiTree", "LumiTree");

    lumitree->Branch("run", &runBranch_, "run/I");
    lumitree->Branch("lumi", &lumiBranch_, "lumi/I");
    lumitree->Branch("nevents", &neventsBranch_, "nevents/I");
    lumitree->Branch("summedWeights", &summedWeightsBranch_, "summedWeights/F");

    // create tree
    tree = FS->make<TTree>("MiniTree", "MiniTree");

    // one off branches
    tree->Branch("run", &runBranch_, "run/I");
    tree->Branch("lumi", &lumiBranch_, "lumi/I");
    tree->Branch("event", &eventBranch_, "event/l");
    tree->Branch("genWeight", &genWeightBranch_, "genWeight/F");
    tree->Branch("rho", &rhoBranch_, "rho/F");
    tree->Branch("nTrueVertices", &nTrueVerticesBranch_, "nTrueVertices/F");
    tree->Branch("NUP", &nupBranch_, "NUP/I");
    tree->Branch("isData", &isDataBranch_, "isData/I");

    // add triggers
    for (auto trigName : triggerNames_) {
        for (auto branch : triggerBranchStrings_) {
            std::string branchName = trigName + branch;
            Int_t branchVal;
            triggerIntMap_.insert(std::pair<std::string, Int_t>(branchName,branchVal));
            std::string branchLeaf = branchName + "/I";
            tree->Branch(branchName.c_str(), &triggerIntMap_[branchName], branchLeaf.c_str());
        }
    }

    // add collections
    for (auto coll : collectionOrder_) {
        for (auto collectionName : collectionNamesMap_[coll]) {
            edm::ParameterSet collectionPSet = collectionPSetMap_[coll].getParameter<edm::ParameterSet>(collectionName);
            MiniTree::AddCollectionToTree(coll,collectionName,collectionPSet);
        }
    }

}

void MiniTree::beginLuminosityBlock(edm::LuminosityBlock const& iEvent, edm::EventSetup const& iSetup) {
    // clear the counters
    runBranch_ = iEvent.run();
    lumiBranch_ = iEvent.luminosityBlock();
    neventsBranch_ = 0;
    summedWeightsBranch_ = 0;
}

void MiniTree::endLuminosityBlock(edm::LuminosityBlock const& iEvent, edm::EventSetup const& iSetup) {
    // fill the lumi tree
    lumitree->Fill();
}

void MiniTree::endJob() { }

template<typename T, typename ObjType>
T MiniTree::Evaluate(std::string branchName, std::string function, ObjType obj) {
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
void MiniTree::AnalyzeCollection(edm::Handle<std::vector<ObjType> > objects, std::string name, const edm::TriggerNames& names) {

    // cleanup from before
    for (auto collectionName: collectionNamesMap_[name]) {
        countMap_[collectionName] = 0;
        // trigger matching
        for (auto trig : triggerNames_) {
            for (auto pdgid : triggerMatchMap_[trig]) {
                if ((pdgid==11 && name=="electrons") ||
                    (pdgid==13 && name=="muons") ||
                    (pdgid==15 && name=="taus") ||
                    (pdgid==22 && name=="photons")) {
                    std::string matchBranchName = name + "_matches_" + trig;
                    intMap_[matchBranchName].clear();
                }
            }
        }
        // branches
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
                bool pass;
                try {
                    pass = selector(object);
                }
                catch (cms::Exception& iException) {
                    iException << "Caught exception in evaluating "
                    << collectionName << " with selection: " << collectionSelections_[collectionName] << ".";
                    throw;
                }
                if (!pass) {
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
            // iterate through each trigger to match
            for (std::string trig : triggerNames_) {
                for (int pdgid : triggerMatchMap_[trig]) {
                    if ((pdgid==11 && name=="electrons") ||
                        (pdgid==13 && name=="muons") ||
                        (pdgid==15 && name=="taus") ||
                        (pdgid==22 && name=="photons")) {
                        std::string matchBranchName = name + "_matches_" + trig;
                        Int_t match = MiniTree::MatchedToTriggerObject<ObjType>(object,trig,names);
                        intMap_[matchBranchName].push_back(match);
                    }
                }
            }
            // iterate through each branch
            for (auto branchName : collectionBranches_[collectionName]) {
                std::string function = branchFunctions_[branchName];
                std::string branchType = branchTypes_[branchName];
                if (branchType=="F") { // Float_t
                    floatMap_[branchName].push_back(MiniTree::Evaluate<Float_t,ObjType>(branchName,function,object));
                }
                else if (branchType=="I") { // Int_t
                    intMap_[branchName].push_back(MiniTree::Evaluate<Int_t,ObjType>(branchName,function,object));
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

template<>
bool MiniTree::MatchedToTriggerObject<reco::Vertex>(reco::Vertex obj, std::string trigName, const edm::TriggerNames& names) {
    return false;
}

template<typename ObjType>
bool MiniTree::MatchedToTriggerObject(ObjType obj, std::string trigName, const edm::TriggerNames& names) {
    bool matched = false;
    size_t trigBit = MiniTree::GetTriggerBit(trigName,names);
    std::string pathToMatch = names.triggerName(trigBit);
    for (auto trigObj : *triggerObjects_) {
       if (abs(trigObj.pdgId()) != abs(obj.pdgId())) continue;
       if (reco::deltaR(trigObj, obj) > 0.5) continue;
       trigObj.unpackPathNames(names);
       std::vector<std::string> allPathNames = trigObj.pathNames(false);
       for (auto pathName : allPathNames) {
           if (pathName.compare(pathToMatch)==0) {
               matched = true;
               return matched;
           }
       }
    }
    return matched;
}

size_t MiniTree::GetTriggerBit(std::string trigName, const edm::TriggerNames& names) {
    std::string trigPathString = triggerNamingMap_[trigName];
    std::regex regexp(trigPathString);
    size_t trigBit = names.size();
    for (size_t i=0; i<names.size(); i++) {
        if (std::regex_match(names.triggerName(i), regexp)) {
            if (trigBit != names.size()) { // if we match more than one
                throw cms::Exception("DuplicateTrigger")
                    << "Second trigger matched for \"" << trigPathString 
                    << "\". First: \"" << names.triggerName(trigBit)
                    << "\"; second: \"" << names.triggerName(i) << "\"." << std::endl;
            }
            trigBit = i;
        }
    }
    if (trigBit == names.size()) {
        throw cms::Exception("UnrecognizedTrigger")
            << "No trigger matched for \"" << trigPathString << "\"." << std::endl;
    }
    return trigBit;
}

void MiniTree::analyze(const edm::Event &iEvent, const edm::EventSetup &iSetup) {
    // first, the lumitree
    edm::Handle<GenEventInfoProduct> genEventInfo;
    iEvent.getByToken(genEventInfoToken_, genEventInfo);
   
    neventsBranch_++;
    genWeightBranch_ = 0.;
    if (genEventInfo.isValid()) {
        genWeightBranch_ = genEventInfo->weight();
    }
    summedWeightsBranch_ += genWeightBranch_;

    // now the actual tree
    isDataBranch_ = isData_;

    eventBranch_ = iEvent.id().event();

    // one off stuff
    edm::Handle<double> rho;
    iEvent.getByToken(rhoToken_,rho);

    edm::Handle<std::vector<PileupSummaryInfo> > pileupSummaryInfo;
    iEvent.getByToken(pileupSummaryInfoToken_, pileupSummaryInfo);

    rhoBranch_ = *rho;
    nTrueVerticesBranch_ = 0;
    if (pileupSummaryInfo.isValid() && pileupSummaryInfo->size()>0) {
        nTrueVerticesBranch_ = pileupSummaryInfo->at(1).getTrueNumInteractions();
    }

    edm::Handle<LHEEventProduct> lheInfo;
    iEvent.getByToken(lheEventProductToken_, lheInfo);

    nupBranch_ = 0;
    if (lheInfo.isValid()) {
        nupBranch_ = lheInfo->hepeup().NUP;
    }

    // triggers
    iEvent.getByToken(triggerBitsToken_, triggerBits_);
    iEvent.getByToken(triggerObjectsToken_, triggerObjects_);
    iEvent.getByToken(triggerPrescalesToken_, triggerPrescales_);

    const edm::TriggerNames& names = iEvent.triggerNames(*triggerBits_);

    for (auto trigName : triggerNames_) {
        size_t trigBit = MiniTree::GetTriggerBit(trigName,names);
        std::string passString = trigName + "Pass";
        std::string prescaleString = trigName + "Prescale";
        triggerIntMap_[passString] = triggerBits_->accept(trigBit);
        triggerIntMap_[prescaleString] = triggerPrescales_->getPrescaleForIndex(trigBit);
    }

    // add collections

    // collection branches
    edm::Handle<reco::VertexCollection> vertices;
    iEvent.getByToken(verticesToken_, vertices);

    edm::Handle<reco::GenParticleCollection> genParticles;
    if (!isData_)
        iEvent.getByToken(genParticlesToken_, genParticles);

    edm::Handle<pat::ElectronCollection> electrons;
    iEvent.getByToken(electronsToken_, electrons);

    edm::Handle<pat::MuonCollection> muons;
    iEvent.getByToken(muonsToken_, muons);

    edm::Handle<pat::TauCollection> taus;
    iEvent.getByToken(tausToken_, taus);

    edm::Handle<pat::PhotonCollection> photons;
    iEvent.getByToken(photonsToken_, photons);

    edm::Handle<pat::JetCollection> jets;
    iEvent.getByToken(jetsToken_, jets);

    edm::Handle<pat::METCollection> mets;
    iEvent.getByToken(metsToken_, mets);

    MiniTree::AnalyzeCollection<reco::Vertex>(vertices,"vertices",names);
    if (!isData_)
        MiniTree::AnalyzeCollection<reco::GenParticle>(genParticles,"genParticles",names);
    MiniTree::AnalyzeCollection<pat::Electron>(electrons,"electrons",names);
    MiniTree::AnalyzeCollection<pat::Muon>(muons,"muons",names);
    MiniTree::AnalyzeCollection<pat::Tau>(taus,"taus",names);
    MiniTree::AnalyzeCollection<pat::Photon>(photons,"photons",names);
    MiniTree::AnalyzeCollection<pat::Jet>(jets,"jets",names);
    MiniTree::AnalyzeCollection<pat::MET>(mets,"mets",names);

    tree->Fill();
}
