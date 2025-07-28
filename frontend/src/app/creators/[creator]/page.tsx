import fs from "fs";
import path from "path";
import { notFound } from "next/navigation";

interface Game {
  id: number;
  cover_image: string;
  title: string;
  links: {
    self: string;
    comments: string;
  };
  authors: Array<{
    name: string;
    url: string;
  }>;
  tags: string[];
}

// This function tells Next.js which paths to pre-render at build time
export async function generateStaticParams() {
  try {
    const dataDir = path.join(process.cwd(), "public", "data");
    if (!fs.existsSync(dataDir)) {
      console.warn("Data directory does not exist:", dataDir);
      return [];
    }

    const creators = fs
      .readdirSync(dataDir)
      .filter((name) => fs.statSync(path.join(dataDir, name)).isDirectory());

    return creators.map((creator) => ({ creator }));
  } catch (error) {
    console.error("Error generating static params:", error);
    return [];
  }
}

// Force this page to be statically generated
export const dynamic = "force-static";
export const revalidate = false; // or a number of seconds for ISR

// Function to get creator data
async function getCreatorData(creator: string) {
  const creatorDir = path.join(process.cwd(), "public", "data", creator);
  let games: Game[] = [];
  let error = null;

  if (fs.existsSync(creatorDir)) {
    const files = fs.readdirSync(creatorDir).filter((f) => f.endsWith(".json"));
    games = files.map((file) =>
      JSON.parse(fs.readFileSync(path.join(creatorDir, file), "utf-8"))
    );
  } else {
    error = `Creator directory not found: ${creator}`;
  }

  return { games, error };
}
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export default async function CreatorPage(props: any) {
  const { creator } = props.params as { creator: string };

  // Get the data for this creator
  const { games, error } = await getCreatorData(creator);

  if (!creator) {
    notFound();
  }

  return (
    <div>
      <h1>Creator: {creator}</h1>
      {error ? (
        <p style={{ color: "red" }}>{error}</p>
      ) : (
        <ul>
          {games.map((game, idx) => (
            <li key={idx}>
              <pre>{JSON.stringify(game, null, 2)}</pre>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
