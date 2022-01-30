import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { DatePipe } from '@angular/common';
import { environment } from '../environments/environment';

import { AppComponent } from './app.component';
import { LoginPageComponent } from './login-page/login-page.component';
import { AppRoutingModule } from './app-routing.module';
import { AuthLayoutComponent } from './shared/components/layouts/auth-layout/auth-layout.component';
import { SiteLayoutComponent } from './shared/components/layouts/site-layout/site-layout.component';
import { RegisterPageComponent } from './register-page/register-page.component';
import { TokenInterceptor } from './shared/services/auth/token.interceptor';
import { LoaderComponent } from './shared/components/loader/loader.component';
import { ClientsPageComponent } from './clients-page/clients-page.component';
import { ClientPageComponent } from './clients-page/client-page/client-page.component';

@NgModule({
    declarations: [
        AppComponent,
        LoginPageComponent,
        AuthLayoutComponent,
        SiteLayoutComponent,
        RegisterPageComponent,
        LoaderComponent,
        ClientsPageComponent,
        ClientPageComponent,
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        FormsModule,
        ReactiveFormsModule,
        HttpClientModule,
    ],
    providers: [
        {
            provide: HTTP_INTERCEPTORS,
            multi: true,
            useClass: TokenInterceptor,
        },
        DatePipe,
    ],
    bootstrap: [AppComponent]
})
export class AppModule { }
