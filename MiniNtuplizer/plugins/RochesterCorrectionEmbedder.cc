// RochesterCorrectionEmbedder.cc

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/PatCandidates/interface/Muon.h"

#include "AnalysisTools/MiniNtuplizer/plugins/rochcor2015.h"
#include "AnalysisTools/MiniNtuplizer/plugins/muresolution_run2.h"

class RochesterCorrectionEmbedder : public edm::stream::EDProducer<>
{
public:
  explicit RochesterCorrectionEmbedder(const edm::ParameterSet&);
  ~RochesterCorrectionEmbedder() {}

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  // Methods
  void beginJob() {}
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  void endJob() {}

  // Data
  edm::EDGetTokenT<edm::View<pat::Muon> > collectionToken_; // input collection
  bool isData_;
  std::auto_ptr<std::vector<pat::Muon> > out;             // Collection we'll output at the end
};

// Constructors and destructors
RochesterCorrectionEmbedder::RochesterCorrectionEmbedder(const edm::ParameterSet& iConfig):
  collectionToken_(consumes<edm::View<pat::Muon> >(iConfig.getParameter<edm::InputTag>("src"))),
  isData_(iConfig.getParameter<bool>("isData"))
{
  produces<std::vector<pat::Muon> >();
}

void RochesterCorrectionEmbedder::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  out = std::auto_ptr<std::vector<pat::Muon> >(new std::vector<pat::Muon>);

  edm::Handle<edm::View<pat::Muon> > collection;
  iEvent.getByToken(collectionToken_, collection);

  std::auto_ptr<rochcor2015> rmcor(new rochcor2015());

  for (size_t c = 0; c < collection->size(); ++c) {
    const auto ptr = collection->ptrAt(c);
    pat::Muon newObj = *ptr;

    TLorentzVector p4;
    p4.SetPtEtaPhiM(ptr->pt(),ptr->eta(),ptr->phi(),ptr->mass());
    int charge = ptr->charge();
    float qter = 1.0; 
    int runopt = 0;
    int ntrk = 0;

    if (isData_) {
      rmcor->momcor_data(p4, charge, runopt, qter);
    }
    else {
      rmcor->momcor_mc(p4, charge, ntrk, qter);
    }

    newObj.addUserFloat("rochesterPt", p4.Pt());
    newObj.addUserFloat("rochesterEta", p4.Eta());
    newObj.addUserFloat("rochesterPhi", p4.Phi());
    newObj.addUserFloat("rochesterEnergy", p4.Energy());
    newObj.addUserFloat("rochesterError", qter);
    out->push_back(newObj);
  }

  iEvent.put(out);
}

void RochesterCorrectionEmbedder::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

DEFINE_FWK_MODULE(RochesterCorrectionEmbedder);
