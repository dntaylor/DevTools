#include "DevTools/Ntuplizer/interface/MiniTree.h"

MiniTree::MiniTree(const edm::ParameterSet &iConfig) :
    lheEventProductToken_(consumes<LHEEventProduct>(iConfig.getParameter<edm::InputTag>("lheEventProduct"))),
    genEventInfoToken_(consumes<GenEventInfoProduct>(iConfig.getParameter<edm::InputTag>("genEventInfo"))),
    rhoToken_(consumes<double>(iConfig.getParameter<edm::InputTag>("rho"))),
    pileupSummaryInfoToken_(consumes<std::vector<PileupSummaryInfo> >(iConfig.getParameter<edm::InputTag>("pileupSummaryInfo"))),
    triggerBitsToken_(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("triggerResults"))),
    filterBitsToken_(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("filterResults"))),
    triggerObjectsToken_(consumes<pat::TriggerObjectStandAloneCollection>(iConfig.getParameter<edm::InputTag>("triggerObjects"))),
    triggerPrescalesToken_(consumes<pat::PackedTriggerPrescales>(iConfig.getParameter<edm::InputTag>("triggerPrescales"))),
    triggerBranches_(iConfig.getParameter<edm::ParameterSet>("triggerBranches")),
    filterBranches_(iConfig.getParameter<edm::ParameterSet>("filterBranches")),
    collections_(iConfig.getParameter<edm::ParameterSet>("collections")),
    vertexCollections_(iConfig.getParameter<edm::ParameterSet>("vertexCollections")),
    isData_(iConfig.getParameter<bool>("isData"))
{
    // Declare use of TFileService
    usesResource("TFileService");
    // get trigger parameters
    triggerBranchStrings_.push_back("Pass");
    triggerBranchStrings_.push_back("Prescale");
    triggerNames_ = triggerBranches_.getParameterNames();
    for (auto trig : triggerNames_) {
        edm::ParameterSet trigPSet = triggerBranches_.getParameter<edm::ParameterSet>(trig);
        std::string trigString = trigPSet.getParameter<std::string>("path");
        triggerNamingMap_.insert(std::pair<std::string, std::string>(trig,trigString));
    }
    // get filter parameters
    filterNames_ = filterBranches_.getParameterNames();
    for (auto trig : filterNames_) {
        edm::ParameterSet trigPSet = filterBranches_.getParameter<edm::ParameterSet>(trig);
        std::string trigString = trigPSet.getParameter<std::string>("path");
        triggerNamingMap_.insert(std::pair<std::string, std::string>(trig,trigString));
    }

    // now build the branches

    edm::Service<TFileService> FS;

    // create lumitree_
    lumitree_ = FS->make<TTree>("LumiTree", "LumiTree");

    lumitree_->Branch("run", &runBranch_, "run/I");
    lumitree_->Branch("lumi", &lumiBranch_, "lumi/I");
    lumitree_->Branch("nevents", &neventsBranch_, "nevents/I");
    lumitree_->Branch("summedWeights", &summedWeightsBranch_, "summedWeights/F");

    // create tree_
    tree_ = FS->make<TTree>("MiniTree", "MiniTree");

    // one off branches
    tree_->Branch("run", &runBranch_, "run/I");
    tree_->Branch("lumi", &lumiBranch_, "lumi/I");
    tree_->Branch("event", &eventBranch_, "event/l");
    tree_->Branch("genWeight", &genWeightBranch_, "genWeight/F");
    tree_->Branch("numWeights", &numWeightsBranch_, "numWeights/I");
    tree_->Branch("genWeights", &genWeightsBranch_);
    tree_->Branch("rho", &rhoBranch_, "rho/F");
    tree_->Branch("nTrueVertices", &nTrueVerticesBranch_, "nTrueVertices/F");
    tree_->Branch("NUP", &nupBranch_, "NUP/I");
    tree_->Branch("numGenJets", &numGenJetsBranch_, "numGenJets/I");
    tree_->Branch("genHT", &genHTBranch_, "genHT/I");
    tree_->Branch("isData", &isDataBranch_, "isData/I");

    // add triggers
    for (auto trigName : triggerNames_) {
        for (auto branch : triggerBranchStrings_) {
            std::string branchName = trigName + branch;
            Int_t branchVal;
            triggerIntMap_.insert(std::pair<std::string, Int_t>(branchName,branchVal));
            std::string branchLeaf = branchName + "/I";
            tree_->Branch(branchName.c_str(), &triggerIntMap_[branchName], branchLeaf.c_str());
        }
    }

    // add filters
    for (auto trigName : filterNames_) {
        Int_t branchVal;
        triggerIntMap_.insert(std::pair<std::string, Int_t>(trigName,branchVal));
        std::string branchLeaf = trigName + "/I";
        tree_->Branch(trigName.c_str(), &triggerIntMap_[trigName], branchLeaf.c_str());
    }

    // add vertices
    auto vertexCollectionNames_ = vertexCollections_.getParameterNames();
    for (auto coll : vertexCollectionNames_) {
        vertexCollectionBranches_.emplace_back(new VertexCollectionBranches(tree_, coll, vertexCollections_.getParameter<edm::ParameterSet>(coll), consumesCollector()));
    }

    // add collections
    auto collectionNames_ = collections_.getParameterNames();
    for (auto coll : collectionNames_) {
        collectionBranches_.emplace_back(new CandidateCollectionBranches(tree_, coll, collections_.getParameter<edm::ParameterSet>(coll), consumesCollector()));
    }
}

MiniTree::~MiniTree() { }

void MiniTree::beginJob() { }

void MiniTree::beginLuminosityBlock(edm::LuminosityBlock const& iEvent, edm::EventSetup const& iSetup) {
    // clear the counters
    runBranch_ = iEvent.run();
    lumiBranch_ = iEvent.luminosityBlock();
    neventsBranch_ = 0;
    summedWeightsBranch_ = 0;
}

void MiniTree::endLuminosityBlock(edm::LuminosityBlock const& iEvent, edm::EventSetup const& iSetup) {
    // fill the lumi tree_
    lumitree_->Fill();
}

void MiniTree::endJob() { }


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
        return 9999;
        //throw cms::Exception("UnrecognizedTrigger")
        //    << "No trigger matched for \"" << trigPathString << "\"." << std::endl;
    }
    return trigBit;
}

void MiniTree::analyze(const edm::Event &iEvent, const edm::EventSetup &iSetup) {
    // first, the lumitree_
    edm::Handle<GenEventInfoProduct> genEventInfo;
    iEvent.getByToken(genEventInfoToken_, genEventInfo);
   
    neventsBranch_++;
    genWeightBranch_ = 0.;
    if (genEventInfo.isValid()) {
        genWeightBranch_ = genEventInfo->weight();
    }
    summedWeightsBranch_ += genWeightBranch_;

    // now the actual tree_
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
    numGenJetsBranch_ = 0;
    genHTBranch_ = 0;
    genWeightsBranch_.clear();
    if (lheInfo.isValid()) {
        nupBranch_ = lheInfo->hepeup().NUP;
        for (int i =0; i<lheInfo->hepeup().NUP; ++i) {
            int absPdgId = TMath::Abs(lheInfo->hepeup().IDUP[i]);
            int status = lheInfo->hepeup().ISTUP[i];
            if (status == 1 && ((absPdgId >= 1 && absPdgId <= 6) || absPdgId == 21)) { // quarks/gluons
                ++numGenJetsBranch_;
            }
            if (lheInfo->hepeup().ISTUP[i] <0 || (absPdgId>5 && absPdgId!=21))  continue;
            double px=lheInfo->hepeup().PUP.at(i)[0];
            double py=lheInfo->hepeup().PUP.at(i)[1];
            double pt=sqrt(px*px+py*py);
            genHTBranch_ += (Float_t)pt;
        }
        for (size_t i=0; i<lheInfo->weights().size(); ++i) {
            genWeightsBranch_.push_back(lheInfo->weights()[i].wgt);
        }
    }
    numWeightsBranch_ = genWeightsBranch_.size();

    // triggers
    iEvent.getByToken(triggerBitsToken_, triggerBits_);
    iEvent.getByToken(filterBitsToken_, filterBits_);
    iEvent.getByToken(triggerObjectsToken_, triggerObjects_);
    iEvent.getByToken(triggerPrescalesToken_, triggerPrescales_);

    const edm::TriggerNames& names = iEvent.triggerNames(*triggerBits_);

    for (auto trigName : triggerNames_) {
        size_t trigBit = MiniTree::GetTriggerBit(trigName,names);
        std::string passString = trigName + "Pass";
        std::string prescaleString = trigName + "Prescale";
        if (trigBit==9999) {
            triggerIntMap_[passString] = -1;
            triggerIntMap_[prescaleString] = -1;
        }
        else {
            triggerIntMap_[passString] = triggerBits_->accept(trigBit);
            triggerIntMap_[prescaleString] = triggerPrescales_->getPrescaleForIndex(trigBit);
        }
    }

    const edm::TriggerNames& filters = iEvent.triggerNames(*filterBits_);

    for (auto trigName : filterNames_) {
        size_t trigBit = MiniTree::GetTriggerBit(trigName,filters);
        if (trigBit==9999) {
            triggerIntMap_[trigName] = -1;
        }
        else {
            triggerIntMap_[trigName] = filterBits_->accept(trigBit);
        }
    }

    // add vertices
    for ( auto& coll : vertexCollectionBranches_ ) {
        coll->fill(iEvent);
    }

    // add collections
    for ( auto& coll : collectionBranches_ ) {
        coll->fill(iEvent);
    }

    // decide if we store it
    // for now, require at least 1 lepton
    bool keep = false;
    for ( auto& coll : collectionBranches_ ) {
        std::string name = coll->getName();
        int count = coll->getCount();
        if (name=="electrons" && count>0)
            keep = true;
        if (name=="muons" && count>0)
            keep = true;
        if (name=="taus" && count>0)
            keep = true;
    }

    if (keep)
        tree_->Fill();
}
