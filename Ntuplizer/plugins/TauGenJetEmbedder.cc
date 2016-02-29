#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/JetReco/interface/GenJet.h"

#include "DataFormats/Math/interface/deltaR.h"

class TauGenJetEmbedder : public edm::stream::EDProducer<> {
  public:
    TauGenJetEmbedder(const edm::ParameterSet& pset);
    virtual ~TauGenJetEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::EDGetTokenT<edm::View<pat::Tau> > srcToken_;
    edm::EDGetTokenT<edm::View<reco::GenJet> > genJetToken_;
    double deltaR_;
    bool excludeLeptons_;
};

TauGenJetEmbedder::TauGenJetEmbedder(const edm::ParameterSet& pset):
  srcToken_(consumes<edm::View<pat::Tau> >(pset.getParameter<edm::InputTag>("src"))),
  genJetToken_(consumes<edm::View<reco::GenJet> >(pset.getParameter<edm::InputTag>("genJets"))),
  deltaR_(pset.getParameter<double>("deltaR")),
  excludeLeptons_(pset.getParameter<bool>("excludeLeptons"))
{
  produces<pat::TauCollection>();
}

void TauGenJetEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::auto_ptr<pat::TauCollection> output(new pat::TauCollection);

  edm::Handle<edm::View<pat::Tau> > input;
  evt.getByToken(srcToken_, input);

  edm::Handle<edm::View<reco::GenJet> > genJets;
  evt.getByToken(genJetToken_, genJets);

  output->reserve(input->size());
  for (size_t i = 0; i < input->size(); ++i) {
    pat::Tau tau = input->at(i);

    edm::Ptr<reco::GenJet> genJet;
    double closest = 999.;
    for (size_t j = 0; j < genJets->size(); ++j) {
      if (excludeLeptons_) {
        bool exclude = false;
        for (auto jetConstituent: genJets->at(j).getGenConstituents()) {
          if (abs(jetConstituent->pdgId())==11 
              || abs(jetConstituent->pdgId())==13
              || abs(jetConstituent->pdgId())==15) {
            exclude = true;
          }
        }
        if (exclude) continue;
      }
      double thisDR = reco::deltaR(tau,genJets->at(j));
      if ((thisDR < deltaR_) && (thisDR < closest)) {
        genJet = genJets->ptrAt(j);
        closest = thisDR;
      }
    }

    tau.addUserCand("genJet", genJet);
    output->push_back(tau);
  }

  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(TauGenJetEmbedder);
