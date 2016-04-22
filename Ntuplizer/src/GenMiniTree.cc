#include "DevTools/Ntuplizer/interface/GenMiniTree.h"

GenMiniTree::GenMiniTree(const edm::ParameterSet &iConfig) :
    lheEventProductToken_(consumes<LHEEventProduct>(iConfig.getParameter<edm::InputTag>("lheEventProduct"))),
    genEventInfoToken_(consumes<GenEventInfoProduct>(iConfig.getParameter<edm::InputTag>("genEventInfo"))),
    pileupSummaryInfoToken_(consumes<std::vector<PileupSummaryInfo> >(iConfig.getParameter<edm::InputTag>("pileupSummaryInfo"))),
    collections_(iConfig.getParameter<edm::ParameterSet>("collections"))
{
    // Declare use of TFileService
    usesResource("TFileService");

    // now build the branches

    edm::Service<TFileService> FS;

    // create lumitree_
    lumitree_ = FS->make<TTree>("LumiTree", "LumiTree");

    lumitree_->Branch("run", &runBranch_, "run/I");
    lumitree_->Branch("lumi", &lumiBranch_, "lumi/I");
    lumitree_->Branch("nevents", &neventsBranch_, "nevents/I");
    lumitree_->Branch("summedWeights", &summedWeightsBranch_, "summedWeights/F");

    // create tree_
    tree_ = FS->make<TTree>("GenMiniTree", "GenMiniTree");

    // one off branches
    tree_->Branch("run", &runBranch_, "run/I");
    tree_->Branch("lumi", &lumiBranch_, "lumi/I");
    tree_->Branch("event", &eventBranch_, "event/l");
    tree_->Branch("genWeight", &genWeightBranch_, "genWeight/F");
    tree_->Branch("numWeights", &numWeightsBranch_, "numWeights/I");
    tree_->Branch("genWeights", &genWeightsBranch_);
    tree_->Branch("nTrueVertices", &nTrueVerticesBranch_, "nTrueVertices/F");
    tree_->Branch("NUP", &nupBranch_, "NUP/I");
    tree_->Branch("numGenJets", &numGenJetsBranch_, "numGenJets/I");
    tree_->Branch("genHT", &genHTBranch_, "genHT/I");

    // add collections
    auto collectionNames_ = collections_.getParameterNames();
    for (auto coll : collectionNames_) {
        collectionBranches_.emplace_back(new CandidateCollectionBranches(tree_, coll, collections_.getParameter<edm::ParameterSet>(coll), consumesCollector()));
    }
}

GenMiniTree::~GenMiniTree() { }

void GenMiniTree::beginJob() { }

void GenMiniTree::beginLuminosityBlock(edm::LuminosityBlock const& iEvent, edm::EventSetup const& iSetup) {
    // clear the counters
    runBranch_ = iEvent.run();
    lumiBranch_ = iEvent.luminosityBlock();
    neventsBranch_ = 0;
    summedWeightsBranch_ = 0;
}

void GenMiniTree::endLuminosityBlock(edm::LuminosityBlock const& iEvent, edm::EventSetup const& iSetup) {
    // fill the lumi tree_
    lumitree_->Fill();
}

void GenMiniTree::endJob() { }

void GenMiniTree::analyze(const edm::Event &iEvent, const edm::EventSetup &iSetup) {
    // first, the lumitree_
    edm::Handle<GenEventInfoProduct> genEventInfo;
    iEvent.getByToken(genEventInfoToken_, genEventInfo);

    neventsBranch_++;
    genWeightBranch_ = 0.;
    if (genEventInfo.isValid()) {
        genWeightBranch_ = genEventInfo->weight();
    }
    summedWeightsBranch_ += genWeightBranch_;

    eventBranch_ = iEvent.id().event();

    edm::Handle<std::vector<PileupSummaryInfo> > pileupSummaryInfo;
    iEvent.getByToken(pileupSummaryInfoToken_, pileupSummaryInfo);

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

    // add collections
    for ( auto& coll : collectionBranches_ ) {
        coll->fill(iEvent);
    }

    // decide if we store it
    // for now, keep everything
    bool keep = true;

    if (keep)
        tree_->Fill();
}

