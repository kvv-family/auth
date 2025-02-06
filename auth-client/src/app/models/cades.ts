interface AboutModel {}

interface CadesGenerators {
  'CAdESCOM.About': Promise<AboutModel>;
}
type MyCallback = (
  args: any
) => Generator<CadesGenerators[keyof CadesGenerators]>;

export interface CadesPluginModel {
  async_spawn(arg: MyCallback): void;
  CreateObjectAsync<T extends keyof CadesGenerators>(
    arg: T
  ): CadesGenerators[T];
  getLastError(error: any): string;
}
