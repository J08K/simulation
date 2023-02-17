import Head from 'next/head';
import Board from "components/board";
import styles from "../styles/index.module.scss";
import { useState } from 'react';
import EntityList from '@/components/entityList/index';
import { EntityLocation, test_entity_location, SimData} from '@/utils/types';
import EntitySidebar from "@/components/sidebar/currentEntity/entity";
import DBConn from "@/components/sidebar/dbConn/dbConn";

export default function Home() {

  let [selected_entity, setSelectedEntity] = useState<EntityLocation | null>(null);
  let [SimData, setSimData] = useState<SimData | null>(null);

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
          </div>
          <div className='main'>
            <Board grid_size={3} board_data={SimData !== null ? SimData.board : null } onEntitySelect={(entity : EntityLocation) => {setSelectedEntity(entity)}}/>
            <EntityList entity_locations={SimData !== null ? SimData.board.entities : null}/>
          </div>
          <div>
            <EntitySidebar selected={selected_entity} onDeselect={() => {setSelectedEntity(null); console.log("Triggered!")}}/>
          </div>
        </div>
      </main>
    </>
  )
}
