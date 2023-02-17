import Head from 'next/head';
import styles from "../styles/index.module.scss";
import { useState } from 'react';
import { EntityLocation, SimData} from '@/utils/types';
import Board from "@/components/center/board";
import EntityList from '@/components/center/entityList';
import EntitySidebar from "@/components/sidebar/currentEntity";
import DBConn from "@/components/sidebar/dbConn";
import SimInfo from '@/components/sidebar/simInfo';

export default function Home() {

  let [selected_entity, setSelectedEntity] = useState<EntityLocation | null>(null);
  let [sim_data, setSimData] = useState<SimData | null>(null);

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
          <div>
            <DBConn setter={setSimData}/>
            <SimInfo sim_data={sim_data} />
          </div>
          <div className='main'>
            <Board board_data={sim_data !== null ? sim_data.board : null } onEntitySelect={(entity : EntityLocation) => {setSelectedEntity(entity)}}/>
            <EntityList entity_locations={sim_data !== null ? sim_data.board.entities : null}/>
          </div>
          <div>
            <EntitySidebar selected={selected_entity} onDeselect={() => {setSelectedEntity(null); console.log("Triggered!")}}/>
          </div>
        </div>
      </main>
    </>
  )
}
