import { Injectable } from '@angular/core';
import { CadesPluginModel } from '../models/cades';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class CadesService {
  cadesplugin: CadesPluginModel | undefined;
  ProviderName = 'Crypto-Pro GOST R 34.10-2012 Cryptographic Service Provider';
  ProviderType = 80;
  version: BehaviorSubject<null | string>;
  errorMessage: string | null = null;

  constructor() {
    this.version = new BehaviorSubject<null | string>(null);
    if ('cadesplugin' in window) {
      (window.cadesplugin as Promise<any>).then((data: any) => {
        if ('cadesplugin' in window) {
          this.cadesplugin = window.cadesplugin as CadesPluginModel;
          const self = this;
          this.cadesplugin.async_spawn(function* () {
            if (self.cadesplugin) {
              try {
                const oAbout = yield self.cadesplugin.CreateObjectAsync(
                  'CAdESCOM.About'
                );
                self.cadesplugin.CreateObjectAsync('CAdESCOM.About');
                const oVersion = yield oAbout.CSPVersion(
                  self.ProviderName,
                  self.ProviderType
                );

                const Version = yield oVersion.toString();
                self.version.next(Version);
              } catch (err: any) {
                const error = self.cadesplugin.getLastError(err);
                if (error.indexOf('0x80090019') + 1)
                  self.errorMessage = 'Указанный CSP не установлен';
                else self.errorMessage = error;
              }
            }
          });
        }
      });
    }
  }
}
