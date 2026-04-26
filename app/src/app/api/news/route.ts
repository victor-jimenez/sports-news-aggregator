import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET() {
  try {
    // Absolute path to the summarized_news.json file
    const filePath = path.join(process.cwd(), '..', '..', 'summarized_news.json');

    // If we are running from the app directory, the file is two levels up
    // Let's try a few variations to ensure we find it
    let content;
    const possiblePaths = [
      path.join(process.cwd(), 'summarized_news.json'),
      path.join(process.cwd(), '..', 'summarized_news.json'),
      path.join(process.cwd(), '..', '..', 'summarized_news.json'),
    ];

    for (const p of possiblePaths) {
      if (fs.existsSync(p)) {
        content = fs.readFileSync(p, 'utf8');
        break;
      }
    }

    if (!content) {
      return NextResponse.json({ error: 'News data not found' }, { status: 404 });
    }

    const news = JSON.parse(content);
    return NextResponse.json(news);
  } catch (error) {
    console.error('Error reading news file:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
