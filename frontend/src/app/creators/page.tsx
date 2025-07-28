import fs from "fs";
import path from "path";
import Link from "next/link";

export default function CreatorsListPage() {
  const dataDir = path.join(process.cwd(), "public", "data");
  const creators = fs
    .readdirSync(dataDir)
    .filter((name) => fs.statSync(path.join(dataDir, name)).isDirectory());

  return (
    <div>
      <h1>All Creators</h1>
      <ul>
        {creators.map((creator) => (
          <li key={creator}>
            <Link href={`/creators/${creator}`}>{creator}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
