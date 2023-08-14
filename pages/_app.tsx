import { Toaster } from 'react-hot-toast';
import { QueryClient, QueryClientProvider } from 'react-query';

import { appWithTranslation } from 'next-i18next';
import type { AppProps } from 'next/app';
import { Inter } from 'next/font/google';

import Cookies from "universal-cookie";
import '@/styles/globals.css';
import { getToken } from '@/utils/data/cookies';

const inter = Inter({ subsets: ['latin'] });

function App({ Component, pageProps }: AppProps<{}>) {

  if ((getToken() == null) && (typeof window !== 'undefined'))
  {
    window.location.href = "http://localhost:3001/";
  }

  const queryClient = new QueryClient();

  return (
    <div className={inter.className}>
      <Toaster />
      <QueryClientProvider client={queryClient}>
        <Component {...pageProps} />
      </QueryClientProvider>
    </div>
  );
}

// App.getInitialProps = async (appContext: AppContext): Promise<AppInitialProps> => {
//   const appProps = await App.getInitialProps(appContext);
//   const req = appContext.ctx.req;
//   if (req) {
//     // Get cookies from the request object
//     const cookies = req.headers.cookie;
//     // Do something with the cookies here
//   }
//   return { ...appProps };
// };

export default appWithTranslation(App);
