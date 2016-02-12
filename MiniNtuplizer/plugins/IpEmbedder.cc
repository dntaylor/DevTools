// IpEmbedder.cc
// Embed the rho for each event as a user float

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

template<typename T>
class IpEmbedder : public edm::stream::EDProducer<>
{
public:
  explicit IpEmbedder(const edm::ParameterSet&);
  ~IpEmbedder() {}

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  // Methods
  void beginJob() {}
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  void endJob() {}

  double dz(edm::Ptr<T> obj, const reco::Vertex&) { return 0.; }
  double dxy(edm::Ptr<T> obj, const reco::Vertex&) { return 0.; }
  double dB2D(edm::Ptr<T> obj) { return 0.; }
  double dB3D(edm::Ptr<T> obj) { return 0.; }
  double edB2D(edm::Ptr<T> obj) { return 0.; }
  double edB3D(edm::Ptr<T> obj) { return 0.; }

  // Data
  edm::EDGetTokenT<edm::View<T> > collectionToken_;      // input collection
  edm::EDGetTokenT<reco::VertexCollection> vertexToken_; // pv collection
  std::auto_ptr<std::vector<T> > out;                    // Collection we'll output at the end
};

// Constructors and destructors
template<typename T>
IpEmbedder<T>::IpEmbedder(const edm::ParameterSet& iConfig):
  collectionToken_(consumes<edm::View<T> >(iConfig.getParameter<edm::InputTag>("src"))),
  vertexToken_(consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vertexSrc")))
{
  produces<std::vector<T> >();
}

template<typename T>
void IpEmbedder<T>::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  out = std::auto_ptr<std::vector<T> >(new std::vector<T>);

  edm::Handle<edm::View<T> > collection;
  iEvent.getByToken(collectionToken_, collection);

  edm::Handle<reco::VertexCollection> vertices;
  iEvent.getByToken(vertexToken_, vertices);

  const reco::Vertex& pv = *vertices->begin();

  for (size_t c = 0; c < collection->size(); ++c) {
    const auto ptr = collection->ptrAt(c);
    T newObj = *ptr;

    newObj.addUserFloat("dz", dz(ptr, pv));
    newObj.addUserFloat("dxy", dxy(ptr, pv));
    newObj.addUserFloat("dB2D", dB2D(ptr));
    newObj.addUserFloat("dB3D", dB3D(ptr));
    newObj.addUserFloat("edB2D", edB2D(ptr));
    newObj.addUserFloat("edB3D", edB3D(ptr));
    out->push_back(newObj);
  }

  iEvent.put(out);
}

template<>
double IpEmbedder<pat::Electron>::dz(edm::Ptr<pat::Electron> ptr, const reco::Vertex& pv) {
  return ptr->gsfTrack()->dz(pv.position());
}

template<>
double IpEmbedder<pat::Muon>::dz(edm::Ptr<pat::Muon> ptr, const reco::Vertex& pv) {
  return ptr->muonBestTrack()->dz(pv.position());
}

template<>
double IpEmbedder<pat::Tau>::dz(edm::Ptr<pat::Tau> ptr, const reco::Vertex& pv) {
    pat::PackedCandidate const* packedLeadTauCand = dynamic_cast<pat::PackedCandidate const*>(ptr->leadChargedHadrCand().get());
    return packedLeadTauCand->dz();
}

template<>
double IpEmbedder<pat::Electron>::dxy(edm::Ptr<pat::Electron> ptr, const reco::Vertex& pv) {
  return ptr->gsfTrack()->dxy(pv.position());
}

template<>
double IpEmbedder<pat::Muon>::dxy(edm::Ptr<pat::Muon> ptr, const reco::Vertex& pv) {
  return ptr->muonBestTrack()->dxy(pv.position());
}

template<>
double IpEmbedder<pat::Tau>::dxy(edm::Ptr<pat::Tau> ptr, const reco::Vertex& pv) {
    pat::PackedCandidate const* packedLeadTauCand = dynamic_cast<pat::PackedCandidate const*>(ptr->leadChargedHadrCand().get());
    return packedLeadTauCand->dxy();
}

template<>
double IpEmbedder<pat::Electron>::dB2D(edm::Ptr<pat::Electron> ptr) {
    return ptr->dB(pat::Electron::PV2D);
}

template<>
double IpEmbedder<pat::Muon>::dB2D(edm::Ptr<pat::Muon> ptr) {
    return ptr->dB(pat::Muon::PV2D);
}

template<>
double IpEmbedder<pat::Electron>::dB3D(edm::Ptr<pat::Electron> ptr) {
    return ptr->dB(pat::Electron::PV3D);
}

template<>
double IpEmbedder<pat::Muon>::dB3D(edm::Ptr<pat::Muon> ptr) {
    return ptr->dB(pat::Muon::PV3D);
}

template<>
double IpEmbedder<pat::Electron>::edB2D(edm::Ptr<pat::Electron> ptr) {
    return ptr->edB(pat::Electron::PV2D);
}

template<>
double IpEmbedder<pat::Muon>::edB2D(edm::Ptr<pat::Muon> ptr) {
    return ptr->edB(pat::Muon::PV2D);
}

template<>
double IpEmbedder<pat::Electron>::edB3D(edm::Ptr<pat::Electron> ptr) {
    return ptr->edB(pat::Electron::PV3D);
}

template<>
double IpEmbedder<pat::Muon>::edB3D(edm::Ptr<pat::Muon> ptr) {
    return ptr->edB(pat::Muon::PV3D);
}

template<typename T>
void IpEmbedder<T>::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
typedef IpEmbedder<pat::Electron> ElectronIpEmbedder;
typedef IpEmbedder<pat::Muon> MuonIpEmbedder;
typedef IpEmbedder<pat::Tau> TauIpEmbedder;

DEFINE_FWK_MODULE(ElectronIpEmbedder);
DEFINE_FWK_MODULE(MuonIpEmbedder);
DEFINE_FWK_MODULE(TauIpEmbedder);
