import Head from 'next/head'
import { Inter } from '@next/font/google'
import Board from "components/board"

const inter = Inter({ subsets: ['latin'] })

export default function Home() {
  return (
    <>
      <Head>
        <title>Simulation Analytics</title>
        <meta name="description" content="Simulation statistics." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main>
        Hello, World!
        <Board width={16} height={10}/>
      </main>
    </>
  )
}
