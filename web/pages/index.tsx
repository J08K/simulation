import Head from 'next/head';
import Board from "components/board";
import styles from "../styles/index.module.scss";
import { useState } from 'react';
import { EntityLocation } from '@/utils/types';

export default function Home() {

  let [entity_locations, update_locations] = useState([]);

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
          <div className='main'>
            <Board width={16} height={10} grid_size={3} entity_locations={entity_locations}/>
            
          </div>
          <div></div>
        </div>
      </main>
    </>
  )
}
