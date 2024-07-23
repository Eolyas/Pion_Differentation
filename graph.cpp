#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <TCanvas.h>
#include <TGraph.h>
#include <TAxis.h>



using namespace std;


int main() {

    string name, title, data, xaxis, yaxis, newtitle;

    vector<double> xData, yData;

    cout<<"File data name\n>>> "; cin>>data;

    ifstream dataFile(data);

    if (!dataFile.is_open()) {
        cout << "Erreur : Impossible to open file." << endl;
        return 1;
    }

    // Data read from file
    double x, y;
    while (dataFile >> x >> y) {
        xData.push_back(x);
        yData.push_back(y);
    }

    dataFile.close();

    TCanvas *canvas = new TCanvas("canvas", "Graph", 800, 600);
    auto graph = new TGraph(xData.size(), &xData[0], &yData[0]);

    graph->SetTitle("Graph");
    graph->SetMarkerStyle(20);
    graph->SetMarkerColor(kBlue);
    graph->SetLineColor(kRed);
    //canvas->SetLogx();
    //canvas->SetLogy();

    graph->Draw("APL");
    canvas->Update();


    cout<<"Savefile name\n>>> "; cin>>name;
    cin.ignore(); // This line is very important. Without it we litteraly can't write titles which are overwritten by \n

    cout<<"x axis\n>>> "; getline(cin,xaxis);
    cout<<xaxis<<endl;

    cout<<"y axis\n>>> "; getline(cin,yaxis);
    cout<<yaxis<<endl;

    cout<<"Graph's title\n>>> "; getline(cin,title);
    cout<<title<<endl;

    graph->GetXaxis()->SetTitle(xaxis.c_str());
    graph->GetYaxis()->SetTitle(yaxis.c_str());


    newtitle= title +";"+xaxis+";"+yaxis;
    graph->SetTitle(newtitle.c_str());
    canvas->Print(name.c_str());



    delete graph;
    delete canvas;

    return 0;
}
