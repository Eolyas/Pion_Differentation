#include <TFile.h>
#include <TH1.h>
#include <iostream>
#include <fstream>
using namespace std;

/*Program that create an histogram based on a variable and data extracted from a ROOT file from the simulation*/

void data_create(const char* data,const char* histo,const char* output){

    // Ouvrir le fichier ROOT
    TFile *file = TFile::Open(data);

    // Vérifier si le fichier est ouvert correctement
    if (!file || file->IsZombie()) {
        std::cerr << "Error when opening the ROOT file." << std::endl;
    }


     TH1 *histogram = dynamic_cast<TH1*>(file->Get(histo));

    // Vérifier si l'histogramme est récupéré correctement
    if (!histogram) {
        std::cerr << "Impossible to find the histogram ROOT file." << std::endl;
        file->Close();
    }


    //Double_t somme = histogram->Integral(1, -2);
    Double_t somme = histogram->GetMean();
    //Double_t max= histogram ->  GetMaximum();
    cout << somme << endl;
    //cout << max << endl;
    // Fermer le fichier ROOT
    file->Close();

    ofstream fichier(output, std::ios_base::app);

     if (!fichier.is_open()) {
        // Le fichier n'existe pas, donc on le crée
        fichier.open(output);
        }

fichier << "4.5\t" << somme << std::endl;
    fichier.close();





     /*ofstream fichier1("max.txt", std::ios_base::app);

     if (!fichier1.is_open()) {
        // Le fichier n'existe pas, donc on le crée
        fichier1.open("max.txt");
        }



fichier1 << "400\t" << max << std::endl;
    fichier1.close(); */

}

int main(){
#data_create("output/modules.root","DetectorHistogrammer/Detector/cluster_size/cluster_size","mu+.txt");
    //data_create("output/modules.root","DetectorHistogrammer/detector/charge/cluster_charge","cluster_charge.txt");
    data_create("output/modules.root","DetectorHistogrammer/detector/charge/total_charge","total_charge.txt");
    return 0;
}
