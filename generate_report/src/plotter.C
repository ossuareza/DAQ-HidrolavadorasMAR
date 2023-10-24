#include <iostream>

#include "TCanvas.h"
#include "TROOT.h"
#include "TF1.h"
#include <TGraph.h>

#include <iostream>
#include <fstream>
#include <string>



Double_t *graph_generator(const char *title, int n, double *x, double *y, const char *path){

    TCanvas *c = new TCanvas("c", "Dynamic Filling Example", 200, 10, 1500, 500);
    c->SetGrid();
    auto graph = new TGraph(n,x,y);

    graph->SetTitle(title);

    // Make the plot estetically better
    graph->SetMarkerStyle(kOpenCircle);
    graph->SetMarkerColor(kBlack);
    
    graph->Draw("AP");

    TF1 *fitFunction = new TF1("fitFunction", "pol3", 0, 200);

    fitFunction->SetLineColor(kBlue);
    
    // Perform the fit
    graph->Fit(fitFunction, "Q"); // "Q" for quiet mode

    // Extract fit results
    TF1 *myfunc = graph->GetFunction("fitFunction");
    Double_t *parameters = myfunc->GetParameters();

    c->Print(path);

    return parameters;
}


void plotter(){
//    std::fstream newfile;
//    newfile.open("data/measurments/measurments.txt",ios::out);  // open a file to perform write operation using file object

//    if(newfile.is_open()){ //checking whether the file is open {
//       newfile<<"Tutorials point \n"; //inserting text
//       newfile<<"Tutorials point \n";
//       newfile.close(); //close the file object
//    }
//    newfile.open("data/measurments/measurments.txt",ios::in); //open a file to perform read operation using file object
//    if (newfile.is_open()){ //checking whether the file is open
//       string tp;
//       while(getline(newfile, tp)){ //read data from file object and put it into string.
//          cout << tp << "\n"; //print the data of the string
//       }
//       newfile.close(); //close the file object.
//    }


    // The values and the errors on the Y axis
    const int n_points=10;
    double flow[n_points]=
            {1,2,3,4,5,6,7,8,9,10};
    double pump_power[n_points]=
            {6,12,14,20,22,24,35,45,44,53};
    double head[n_points]=
            {55, 54.5, 54, 53, 52.5, 51.7, 50, 48.5, 46, 44};
    double efficiency[n_points]=
            {0,10,20,20,25,30,40,70,60,50};


    // TCanvas *c1 = new TCanvas("c1", "Dynamic Filling Example", 200, 10, 1500, 500);
    // c1->SetGrid();
    // int n = 10;
    // auto graph = new TGraph(n,flow,head);

    // graph->SetTitle("Flujo vs Potencia;Flujo (m^3/s);Potencia (kW)");

    // // Make the plot estetically better
    // graph->SetMarkerStyle(kOpenCircle);
    // graph->SetMarkerColor(kBlack);
    
    // graph->Draw("AP");

    // TF1 *fitFunction = new TF1("fitFunction", "pol3", 0, 200);

    // fitFunction->SetLineColor(kBlue);
    
    // // Perform the fit
    // graph->Fit(fitFunction, "Q"); // "Q" for quiet mode

    // // Extract fit results
    // TF1 *myfunc = graph->GetFunction("fitFunction");
    // Double_t *parameters = myfunc->GetParameters();


    /* TCanvas *c1 = new TCanvas("c1", "Dynamic Filling Example", 200, 10, 1500, 500);
    c1->SetGrid();
    int n = 10;
    auto graph = new TGraph(n,flow,head);

    Double_t *parameters = graph_generator(graph);


    std::cout << parameters[0] << parameters[1] << parameters[2] << parameters[3] <<parameters[4] <<std::endl;

    c1->Print("data/imgs/FlowVsPower.png"); */

    int n = 10;
    const char* title1 = "Flujo vs Potencia;Flujo (m^3/s);Potencia (kW)";
    const char* path1 = "data/imgs/FlowVsPower.png";
    Double_t *parameters = graph_generator(title1, n, flow, pump_power, path1);

    const char* title2 = "Flujo vs Cabeza;Flujo (m^3/s); Cabeza (m)";
    const char* path2 = "data/imgs/FlowVsHead.png";
    Double_t *parameters2 = graph_generator(title1, n, flow, head, path2);

    const char* title3 = "Flujo vs Eficiencia;Flujo (m^3/s); Eficiencia (%)";
    const char* path3 = "data/imgs/FlowVsEfficiency.png";
    Double_t *parameters3 = graph_generator(title1, n, flow, efficiency, path3);


    // TCanvas *c2 = new TCanvas("c1", "Dynamic Filling Example", 200, 10, 1500, 500);
    // c2 ->SetGrid();

    // auto graph2 = new TGraph(n,flow,head);
    // graph2->SetTitle("Flujo vs Cabeza;Flujo (m^3/s); Cabeza (m)");

    // // Make the plot estetically better
    // graph2->SetMarkerStyle(kOpenCircle);
    // graph2->SetMarkerColor(kBlue);
    // graph2->Draw("AP");

    // c2->Print("data/imgs/FlowVsHead.png");

    // TCanvas *c3 = new TCanvas("c1", "Dynamic Filling Example", 200, 10, 1500, 500);
    // c3->SetGrid();

    // auto graph3 = new TGraph(n,flow,efficiency);
    // graph3->SetTitle("Flujo vs Eficiencia;Flujo (m^3/s); Eficiencia (%)");

    // // Make the plot estetically better
    // graph3->SetMarkerStyle(kOpenCircle);
    // graph3->SetMarkerColor(kBlue);
    // graph3->SetLineColor(kBlue);
    // graph3->SetFillColor(0);

    // graph3->Draw("AP");
    // c3->Print("data/imgs/FlowVsEfficiency.png");
}

