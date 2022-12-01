#include "TTree.h"
#include "TH1D.h"

void hist(){

    Int_t NBINS = 45;
    Float_t MIN = 10;
    Float_t MAX = 55;

    // read data, create tree and histogram
    TTree *t1 = new TTree("t1", "the tree 1");

    t1->ReadFile("results1e5.out", "occ");
    Float_t occ;
    t1->SetBranchAddress("occ", &occ);

    TH1D *h1 = new TH1D("h1", "Distribuzione metodo di Montecarlo",
                        NBINS, MIN, MAX);

    // read all entries and fill the histogram
    Long64_t nentries = t1->GetEntries();
    for (Long64_t i=0; i<nentries; i++) {
        t1->GetEntry(i);
        h1->Fill(occ);
    }

    TF1 *f1 = new TF1("f1", "gaus", MIN, MAX);
    TFitResultPtr r = h1->Fit("f1", "IRMS");

    // double likelihood_value = r->MinFcnValue();
    gStyle->SetOptFit(1111);

    h1->SetTitle("Montecarlo simulation");
    h1->GetXaxis()->SetTitle("Particelle passate per i 3 scintillatori [2e-2]");
    h1->GetYaxis()->SetTitle("Occorrenze");
    h1->SetLineColor(kBlue);
    h1->Draw();
}