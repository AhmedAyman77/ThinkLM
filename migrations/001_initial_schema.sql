create extension if not exists "uuid-ossp";

create table users (
    id uuid primary key default uuid_generate_v4(),
    name text not null,
    email text unique not null,
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);

create table conversations (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid references users(id) on delete cascade,
    title text,
    created_at timestamptz default now()
);

create table messages (
    id uuid primary key default uuid_generate_v4(),
    conversation_id uuid references conversations(id) on delete cascade,
    role text check (role in ('user', 'assistant')) not null,
    content text not null,
    modality text check (modality in ('text', 'voice')) default 'text',
    intent text check (intent in ('RAG_QUERY', 'SUMMARIZE', 'TRANSLATE', 'DIRECT_LLM')),
    created_at timestamptz default now()
);

create table files (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid references users(id) on delete cascade,
    file_name text not null,
    mime_type text not null,
    status text check (status in ('processing', 'ready', 'failed')) default 'processing',
    chunks_count integer default 0,
    collection_name text,
    raw_text_path text,
    created_at timestamptz default now()
);