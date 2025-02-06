import { HttpClient } from '@angular/common/http';

interface LocalConfiguration {
  issuer: string;
  authorization_endpoint: string;
  token_endpoint: string;
  userinfo_endpoint: string;
  jwks_uri: string;
}

class PathAuth {
  configurationPath: string = '/.well-known/openid-configuration';
  configuration: LocalConfiguration | undefined;
  loaded: boolean = false;

  add(configuration: LocalConfiguration) {
    this.configuration = configuration;
    this.loaded = true;
  }
}

export class LocalModel {
  _baseUrl: string;
  _http: HttpClient;
  _paths: PathAuth;

  constructor(http: HttpClient, baseUrl: string) {
    this._baseUrl = baseUrl;
    this._http = http;
    this._paths = new PathAuth();
  }

  getUrl(dop: string): string {
    return `${this._baseUrl}${dop}`;
  }

  getConfiguration() {
    this._http
      .get(this.getUrl(this._paths.configurationPath))
      .subscribe((data) => {
        this._paths.add(data as LocalConfiguration);
      });
  }

  authorize(username: string, password: string) {
    if (this._paths.loaded && this._paths.configuration) {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);
      formData.append('form', 'api');
      this._http
        .post(this._paths.configuration.authorization_endpoint, formData)
        .subscribe((data) => {
          console.log(data);
        });
    }
  }
}
