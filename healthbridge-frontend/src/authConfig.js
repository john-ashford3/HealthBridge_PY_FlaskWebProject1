export const msalConfig = {
  auth: {
    clientId: 'your-client-id',
    authority: 'https://your-tenant-name.b2clogin.com/your-tenant-name.onmicrosoft.com/B2C_1_signupsignin1',
    redirectUri: 'http://localhost:3000',
  },
  cache: {
    cacheLocation: 'sessionStorage',
    storeAuthStateInCookie: false,
  }
};