#include <iostream>
#include "TGraph.h"

#include "TCanvas.h"
#include "TROOT.h"
#include "TGraphErrors.h"
#include "TF1.h"
#include "TLegend.h"
#include "TArrow.h"
#include "TLatex.h"

#include <iostream>
#include <fstream>
#include <string>


void macro1(){
   std::fstream newfile;
   newfile.open("tpoint.txt",ios::out);  // open a file to perform write operation using file object

   if(newfile.is_open()){ //checking whether the file is open {
      newfile<<"Tutorials point \n"; //inserting text
      newfile<<"Tutorials point \n";
      newfile.close(); //close the file object
   }
   newfile.open("tpoint.txt",ios::in); //open a file to perform read operation using file object
   if (newfile.is_open()){ //checking whether the file is open
      string tp;
      while(getline(newfile, tp)){ //read data from file object and put it into string.
         cout << tp << "\n"; //print the data of the string
      }
      newfile.close(); //close the file object.
   }




    // The values and the errors on the Y axis
    const int n_points=10;
    double flow[n_points]=
            {1,2,3,4,5,6,7,8,9,10};
    double pump_power[n_points]=
            {6,12,14,20,22,24,35,45,44,53};
    double head[n_points]=
            {5,5,4.7,4.5,4.2,5.1,2.9,4.1,4.8,5.43};
    double efficiency[n_points]=
            {0,10,20,20,25,30,40,70,60,50};


    TCanvas *c1 = new TCanvas("c1", "Dynamic Filling Example", 200, 10, 1500, 500);
    c1->SetGrid();
    int n = 10;
    
    auto graph = new TGraph(n,flow,pump_power);
    graph->SetTitle("Flujo vs Potencia;Flujo (m^3/s);Potencia (kW)");

    // Make the plot estetically better
    graph->SetMarkerStyle(kOpenCircle);
    graph->SetMarkerColor(kBlue);
    graph->SetLineColor(kBlue);
    graph->SetFillColor(0);

    graph->Draw("AC*");

    c1->Print("FlowVsPower.png");



    TCanvas *c2 = new TCanvas("c1", "Dynamic Filling Example", 200, 10, 1500, 500);
    c2 ->SetGrid();

    auto graph2 = new TGraph(n,flow,head);
    graph2->SetTitle("Flujo vs Cabeza;Flujo (m^3/s); Cabeza (m)");

    // Make the plot estetically better
    graph2->SetMarkerStyle(kOpenCircle);
    graph2->SetMarkerColor(kBlue);
    graph2->SetLineColor(kBlue);
    graph2->SetFillColor(0);

    graph2->Draw("AC*");

    c2->Print("FlowVsHead.png");

    TCanvas *c3 = new TCanvas("c1", "Dynamic Filling Example", 200, 10, 1500, 500);
    c3->SetGrid();

    auto graph3 = new TGraph(n,flow,efficiency);
    graph3->SetTitle("Flujo vs Eficiencia;Flujo (m^3/s); Eficiencia (%)");

    // Make the plot estetically better
    graph3->SetMarkerStyle(kOpenCircle);
    graph3->SetMarkerColor(kBlue);
    graph3->SetLineColor(kBlue);
    graph3->SetFillColor(0);

    graph3->Draw("AC*");

    c3->Print("FlowVsEfficiency.png");
}

