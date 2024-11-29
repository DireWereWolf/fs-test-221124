import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import {provideHttpClient} from '@angular/common/http';
import {BrowserModule} from '@angular/platform-browser';
import {NoopAnimationsModule} from '@angular/platform-browser/animations';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import {LocationStrategy, PathLocationStrategy} from '@angular/common';


import { routes } from './app.routes';


export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideHttpClient(),
    { provide: BrowserModule },
    { provide: NoopAnimationsModule }, provideAnimationsAsync('noop'),
    { provide: LocationStrategy, useClass: PathLocationStrategy },
  ]
};
