// system includes
#include <memory>
#include <vector>
#include <iostream>

// CMS includes
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/VIDCutFlowResult.h"

template<typename T>
class VIDEmbedder : public edm::stream::EDProducer<>
{
  public:
    explicit VIDEmbedder(const edm::ParameterSet&);
    ~VIDEmbedder() {}
  
    //static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
  
  private:
    void beginJob() {}
    virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
    void endJob() {}
  
    edm::EDGetTokenT<edm::View<T> > collectionToken_;
    std::vector<std::string> idLabels_;
    std::vector<edm::EDGetTokenT<edm::ValueMap<bool> > > idMapTokens_;
    std::vector<std::string> valueLabels_;
    std::vector<edm::EDGetTokenT<edm::ValueMap<float> > > valueTokens_;
    std::vector<std::string> categoryLabels_;
    std::vector<edm::EDGetTokenT<edm::ValueMap<int> > > categoryTokens_;
    std::auto_ptr<std::vector<T> > out;
};


// Constructors and destructors
template<typename T>
VIDEmbedder<T>::VIDEmbedder(const edm::ParameterSet& iConfig):
  collectionToken_(consumes<edm::View<T> >(iConfig.getParameter<edm::InputTag>("src"))),
  idLabels_(iConfig.exists("idLabels") ? iConfig.getParameter<std::vector<std::string> >("idLabels") : std::vector<std::string>()),
  valueLabels_(iConfig.exists("valueLabels") ? iConfig.getParameter<std::vector<std::string> >("valueLabels") : std::vector<std::string>()),
  categoryLabels_(iConfig.exists("categoryLabels") ? iConfig.getParameter<std::vector<std::string> >("categoryLabels") : std::vector<std::string>())
{
  std::vector<edm::InputTag> idTags = iConfig.getParameter<std::vector<edm::InputTag> >("ids");
  for(unsigned int i = 0; (i < idTags.size() && i < idLabels_.size()); ++i) {
    idMapTokens_.push_back(consumes<edm::ValueMap<bool> >(idTags.at(i)));
  }

  std::vector<edm::InputTag> valueTags = iConfig.getParameter<std::vector<edm::InputTag> >("values");
  for(unsigned int i = 0; (i < valueTags.size() && i < valueLabels_.size()); ++i) {
    valueTokens_.push_back(consumes<edm::ValueMap<float> >(valueTags.at(i)));
  }

  std::vector<edm::InputTag> categoryTags = iConfig.getParameter<std::vector<edm::InputTag> >("categories");
  for(unsigned int i = 0; (i < categoryTags.size() && i < categoryLabels_.size()); ++i) {
    categoryTokens_.push_back(consumes<edm::ValueMap<int> >(categoryTags.at(i)));
  }

  produces<std::vector<T> >();
}

template<typename T>
void VIDEmbedder<T>::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  out = std::auto_ptr<std::vector<T> >(new std::vector<T>);
  
  edm::Handle<edm::View<T> > collection;
  std::vector<edm::Handle<edm::ValueMap<bool> > > ids(idMapTokens_.size(), edm::Handle<edm::ValueMap<bool> >() );
  std::vector<edm::Handle<edm::ValueMap<float> > > values(valueTokens_.size(), edm::Handle<edm::ValueMap<float> >() );
  std::vector<edm::Handle<edm::ValueMap<int> > > categories(categoryTokens_.size(), edm::Handle<edm::ValueMap<int> >() );
  
  iEvent.getByToken(collectionToken_, collection);
  
  for (unsigned int i = 0; i < idMapTokens_.size(); ++i) {
    iEvent.getByToken(idMapTokens_.at(i), ids.at(i));
  }
  for(unsigned int i = 0; i < valueTokens_.size(); ++i) {
    iEvent.getByToken(valueTokens_.at(i), values.at(i));
  }
  for(unsigned int i = 0; i < categoryTokens_.size(); ++i) {
    iEvent.getByToken(categoryTokens_.at(i), categories.at(i));
  }
  
  for (size_t c = 0; c < collection->size(); ++c) {
    const auto obj = collection->at(c);
    const auto ptr = collection->ptrAt(c);
    T newObj = obj;
    
    for(unsigned int i = 0; i < ids.size(); ++i) {
      bool result = (*(ids.at(i)))[ptr];
      newObj.addUserInt(idLabels_.at(i), result);
    }
    for(unsigned int i = 0; i < values.size(); ++i) {
      float result = (*(values.at(i)))[ptr];
      newObj.addUserFloat(valueLabels_.at(i), result);
    }
    for(unsigned int i = 0; i < categories.size(); ++i) {
      int result = (*(categories.at(i)))[ptr];
      newObj.addUserInt(categoryLabels_.at(i), result);
    }
  
    out->push_back(newObj);
  }
  
  iEvent.put(out);
}


//void VIDEmbedder::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
//  edm::ParameterSetDescription desc;
//  desc.setUnknown();
//  descriptions.addDefault(desc);
//}

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Photon.h"

typedef VIDEmbedder<pat::Electron> ElectronVIDEmbedder;
typedef VIDEmbedder<pat::Photon> PhotonVIDEmbedder;

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(ElectronVIDEmbedder);
DEFINE_FWK_MODULE(PhotonVIDEmbedder);
