#include <iostream>

#include "TCanvas.h"
#include "TROOT.h"
#include "TF1.h"
#include <TGraph.h>
#include <TMultiGraph.h>

#include <iostream>
#include <fstream>
#include <string>



double graph_generator(const char *title, int n, double *x, double *y, const char *path, bool print_max){

    TCanvas *c = new TCanvas("c", "Dynamic Filling Example", 200, 10, 1500, 500);
    c->SetGrid(); // Activate the grid
    auto graph = new TGraph(n,x,y); // define the graph with the points

    graph->SetTitle(title);

    // Modify marker
    graph->SetMarkerStyle(kOpenCircle);
    graph->SetMarkerColor(kBlack);
    

    TF1 *fitFunction = new TF1("fitFunction", "pol3", 0, x[n-1]); // (func name, func type, (range))
    // Modify line
    fitFunction->SetLineColor(kBlue);
    
    // Perform the fit
    graph->Fit(fitFunction, "Q"); // quiet mode
    double maximumY = fitFunction->GetMaximum(); // Find the maximum
    double maximumX = fitFunction->GetMaximumX();

    if (print_max){
        auto graph2 = new TGraph();
        graph2->SetPoint(0, maximumX, maximumY);
        graph2->SetMarkerColor(kRed);
        graph2->SetMarkerStyle(kFullCircle);
        // Merge the two graphs in one
        auto mg = new TMultiGraph();
        mg->Add(graph);
        mg->Add(graph2);
        // Define the way the graph is going to be plotted

        mg->SetTitle(title);

        mg->Draw("AP");
        

    }else{
        // Define the way the graph is going to be plotted
        graph->Draw("AP");
    }

    

    // Extract the equation
    // TF1 *myfunc = graph->GetFunction("fitFunction");
    // Double_t *parameters = myfunc->GetParameters(); // Get coefficients from the function
    
    c->Print(path);

    return maximumY;
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
            

    int n = 10;
    const char* title1 = "Flujo vs Potencia;Flujo (m^3/s);Potencia (kW)";
    const char* path1 = "../data/imgs/FlowVsPower.png";
    double maximum = graph_generator(title1, n, flow, pump_power, path1, true);
    std::cout << maximum << std::endl;

    const char* title2 = "Flujo vs Cabeza;Flujo (m^3/s); Cabeza (m)";
    const char* path2 = "../data/imgs/FlowVsHead.png";
    maximum = graph_generator(title2, n, flow, head, path2, true);
    std::cout << maximum << std::endl;

    const char* title3 = "Flujo vs Eficiencia;Flujo (m^3/s); Eficiencia (%)";
    const char* path3 = "../data/imgs/FlowVsEfficiency.png";
    maximum = graph_generator(title3, n, flow, efficiency, path3, true);
    std::cout << maximum << std::endl;
}

