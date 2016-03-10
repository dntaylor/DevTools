// MuonIdEmbedder.cc
// Embeds muons ids as userInts for later

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

class MuonIdEmbedder : public edm::stream::EDProducer<>
{
public:
  explicit MuonIdEmbedder(const edm::ParameterSet&);
  ~MuonIdEmbedder() {}

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  // Methods
  void beginJob() {}
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  void endJob() {}

  // Data
  edm::EDGetTokenT<edm::View<pat::Muon> > collectionToken_; // input collection
  edm::EDGetTokenT<reco::VertexCollection> vertexToken_;  // vertices
  std::auto_ptr<std::vector<pat::Muon> > out;             // Collection we'll output at the end
};

// Constructors and destructors
MuonIdEmbedder::MuonIdEmbedder(const edm::ParameterSet& iConfig):
  collectionToken_(consumes<edm::View<pat::Muon> >(iConfig.getParameter<edm::InputTag>("src"))),
  vertexToken_(consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vertexSrc")))
{
  produces<std::vector<pat::Muon> >();
}

void MuonIdEmbedder::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  out = std::auto_ptr<std::vector<pat::Muon> >(new std::vector<pat::Muon>);

  edm::Handle<edm::View<pat::Muon> > collection;
  iEvent.getByToken(collectionToken_, collection);

  edm::Handle<reco::VertexCollection> vertices;
  iEvent.getByToken(vertexToken_, vertices);

  const reco::Vertex& pv = *vertices->begin();

  for (size_t c = 0; c < collection->size(); ++c) {
    const auto obj = collection->at(c);
    pat::Muon newObj = obj;

    newObj.addUserInt("isTightMuon", obj.isTightMuon(pv));
    newObj.addUserInt("isSoftMuon", obj.isSoftMuon(pv));
    newObj.addUserInt("isHighPtMuon", obj.isHighPtMuon(pv));
    newObj.addUserFloat("segmentCompatibility", muon::segmentCompatibility(obj));
    newObj.addUserInt("isGoodMuon", muon::isGoodMuon(obj, muon::TMOneStationTight));
    int highPurity = 0;
    if (obj.innerTrack().isNonnull()) {
        highPurity = obj.innerTrack()->quality(reco::TrackBase::highPurity);
    }
    newObj.addUserInt("highPurityTrack",highPurity);
    
    out->push_back(newObj);
  }

  iEvent.put(out);
}

void MuonIdEmbedder::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

DEFINE_FWK_MODULE(MuonIdEmbedder);
