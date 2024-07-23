#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <TCanvas.h>
#include <TGraph.h>
#include <TAxis.h>
#include <TLegend.h>
#include <TGraphErrors.h>


using namespace std;

void data_recup(string particle, vector<double>& xData, vector<double>& yData, vector<double>& DyData) {
    xData.clear();
    yData.clear();
    DyData.clear();

    ifstream dataFile(particle);
    double x, y, dy;
    while (dataFile >> x >> y>>dy) {
        xData.push_back(x);
        yData.push_back(y);
        DyData.push_back(dy);

    }
    dataFile.close();
}

int main() {
    string name, title, data, xaxis, yaxis, newtitle;


    //gStyle->SetErrorX(0);
    vector<double> xData, yData,DyData ;
    data_recup("pi+.txt", xData, yData, DyData);
    TCanvas *canvas = new TCanvas("canvas", "Graph", 800, 600);
    auto legend = new TLegend(0.15,0.8,0.3,0.9);
    auto graph1 = new TGraphErrors(xData.size(), &xData[0], &yData[0],0 , &DyData[0] );

    graph1->SetMaximum(30);
    graph1->SetTitle("pi+");
    graph1->SetMarkerStyle(22);
    graph1->SetMarkerColor(kBlue);
    graph1->SetLineColor(kRed);
    legend->AddEntry(graph1, "pi+", "lp");

    graph1->Draw("APL");
    canvas->Update();

    data_recup("kaon+.txt", xData, yData, DyData);
    auto graph2 = new TGraphErrors(xData.size(), &xData[0], &yData[0],0,&DyData[0] );

    graph2->SetTitle("kaon+");
    graph2->SetMarkerStyle(28);
    graph2->SetMarkerColor(kBlue);
    graph2->SetLineColor(kMagenta);
    legend->AddEntry(graph2, "kaon+", "lp");

    graph2->Draw("PL SAME");
    canvas->Update();

    data_recup("mu+.txt", xData, yData, DyData);
    auto graph3 = new TGraphErrors(xData.size(), &xData[0], &yData[0],0, &DyData[0]);

    graph3->SetTitle("mu+");
    graph3->SetMarkerStyle(30);
    graph3->SetMarkerColor(kBlue);
    graph3->SetLineColor(kGreen);
    legend->AddEntry(graph3, "mu+", "lp");

    graph3->Draw("PL SAME");
    legend->Draw();
    canvas->Update();

    cout << "Savefile name\n>>> "; 
    cin >> name;
    cin.ignore();  // cette ligne est très importante. sans elle on peut littéralement pas écrire de titre et il est instantanément remplacé par un "\n"

    cout << "x axis\n>>> "; 
    getline(cin, xaxis);
    cout << xaxis << endl;

    cout << "y axis\n>>> "; 
    getline(cin, yaxis);
    cout << yaxis << endl;

    cout << "Graph's title\n>>> "; 
    getline(cin, title);
    cout << title << endl;

    graph1->GetXaxis()->SetTitle(xaxis.c_str());
    graph1->GetYaxis()->SetTitle(yaxis.c_str());

    newtitle = title + ";" + xaxis + ";" + yaxis;
    graph1->SetTitle(newtitle.c_str());
    canvas->Print(name.c_str());

    delete graph1;
    delete graph2;
    delete graph3;
    delete canvas;

    return 0;
}
