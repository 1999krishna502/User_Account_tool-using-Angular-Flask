import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { EditUserComponent } from './edit-user/edit-user.component';
// import { EditUserComponent } from './edit-user/edit-user.component';

export const routes: Routes = [
    {
        path:'login', component:LoginComponent
    },
    {
        path:'register' , component:RegisterComponent
    },
    {
        path:'dashboard', component:DashboardComponent
    },
    {
        path: 'edit', component:EditUserComponent 
    },
];
