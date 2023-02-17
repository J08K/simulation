import { getCollections } from "@/utils/dbConn";
import { NextApiRequest, NextApiResponse } from "next";

type Data = {
    collections: string[],
}

export default async function handler(
    req: NextApiRequest,
    res: NextApiResponse<Data>
  ) {
    return res.status(200).json({ collections: await getCollections() })
  }