e_mang_trans=0.0020*10^(-3); %[m]
e_mang_neg=0.001*10^(-3); %[m]
visc_c=0; %[m^2/s] Depende de la temperatura. Se debe obtener de la Columna 2 de la tabla de excel 
g=9.798; %[m/s^2] (Ya la tiene en el codigo)
%% Rotodinamicas
%Succión
    L_s_r=0.5; %[m]
    D_s_r=51.8*10^(-3); %[m]
    sum_k_s_r=11.65+0.05; %[-]
    e_s_r=e_mang_trans;
    V_s_r=0; %[m/s] Velocidad succión roto (Ya la tiene en el codigo)
    f_s_r=Haaland(e_s_r,D_s_r,visc_c,V_s_r); %[-]
    hL_s_r=(f_s_r*(L_s_r/D_s_r)+sum_k_s_r)*V_s_r^2/(2*g); %[m] Esta es la cabeza de perdidas de la succión de las roto
%Descarga
    D_d_r=38.8/25.4; %[in]
    sum_k_d_r=11.65+1.5+1.4*(D_d_r^(-0.53)); %[-]
    V_d_r=0; %[m/s] Velocidad descarga roto (Ya la tiene en el codigo)
    hL_d_r=(sum_k_d_r)*V_d_r^2/(2*g); %[m] Esta es la cabeza de perdidas de la descarga de las roto
%% Hidro
%Succión
    L_s_h=2.3; %[m]
    D_s_h=24.8*10^(-3); %[m]
    sum_k_s_h=0.3; %[-]
    e_s_h=e_mang_trans;
    V_s_h=0; %[m/s] Velocidad succión hidro (Ya la tiene en el codigo)
    f_s_h=Haaland(e_s_h,D_s_h,visc_c,V_s_h); %[-]
    hL_s_h=(f_s_h*(L_s_h/D_s_h)+sum_k_s_h)*V_s_h^2/(2*g); %[m] Esta es la cabeza de perdidas de la succión de las hidro
%Descarga
    L_d_h=3; %[m]
    D_d_h=7*10^(-3); %[m]
    e_d_h=e_mang_neg;
    V_d_h=0; %[m/s] Velocidad descarga hidro (Ya la tiene en el codigo)
    f_d_h=Haaland(e_d_h,D_d_h,visc_c,V_d_h); %[-]
    hL_d_h=(f_d_h*(L_d_h/D_d_h))*V_d_h^2/(2*g); %[m] Esta es la cabeza de perdidas de la descarga de las hidro
function f=Haaland(e,D,visc_c,V) %Formula explicita para el f de Haaland
    Re=(D*V)/(visc_c);
    f_raiz=(-1.8*log10(((e/D)/3.7)^1.11+(6.9/Re)))^-1;
    f=f_raiz^2;
end