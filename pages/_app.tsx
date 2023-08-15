import { Toaster } from 'react-hot-toast';
import { QueryClient, QueryClientProvider } from 'react-query';

import { appWithTranslation } from 'next-i18next';
import type { AppProps } from 'next/app';
import { Inter } from 'next/font/google';

import Cookies from "universal-cookie";
import '@/styles/globals.css';
import { getCookieEmail, getToken } from '@/utils/data/cookies';

const inter = Inter({ subsets: ['latin'] });

function App({ Component, pageProps }: AppProps<{}>) {

  if ((getToken() == null) && (typeof window !== 'undefined'))
  {
    window.location.href = "http://localhost:3000/";
  }
  console.log("token: " + getToken());
  console.log("userEmail: " + getCookieEmail());
  const queryClient = new QueryClient();


  // let data = new URLSearchParams();
  // data.append("userEmail", getCookieEmail());
  // fetch('http://219.78.175.160:7000/get-user-email', { mode: 'no-cors', method: "post", body: data })
  // .then(res => {console.log("123", res.text())})
  // .then(data => {
  //     // console.log(data);
  //     // window.alert(data);
  //     // if (data.indexOf("Created") != -1) {
  //     //       props.setEnd(null);
  //     // }
  // })
  // .catch(err => console.log(err));


  // Database: save token
  // let data = new URLSearchParams();
  // data.append("token", getToken());
  // let api = "http://219.78.175.160:7000/" + "get-user-email";
  // fetch(api, { method: "post", body: data })
  //     .then(res => {})
  //     .then(data => {
  //         // console.log(data);
  //         // window.alert(data);
  //         // if (data.indexOf("Created") != -1) {
  //         //       props.setEnd(null);
  //         // }
  //     })
  //     .catch(err => console.log(err));

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
