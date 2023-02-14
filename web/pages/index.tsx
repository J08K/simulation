import Head from 'next/head';
import Board from "components/board";
import styles from "../styles/index.module.scss";

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
        <div className={styles.interface}>
          <div></div>
          <Board width={16} height={10} grid_size={3}/>
          <div></div>
        </div>
      </main>
    </>
  )
}
