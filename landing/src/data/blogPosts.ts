export interface BlogPost {
  slug: string
  category: { id: string; en: string }
  tag: 'growth' | 'copywriting' | 'resource'
  readTime: { id: string; en: string }
  date: string
  isResource?: boolean
  title: { id: string; en: string }
  excerpt: { id: string; en: string }
  sections: {
    heading: { id: string; en: string }
    body: { id: string[]; en: string[] }
    copyBox?: {
      label: { id: string; en: string }
      content: string
    }
  }[]
}

export const blogPosts: BlogPost[] = [
  {
    slug: 'algoritma-threads-reply-velocity',
    category: { id: 'ALGORITMA & GROWTH', en: 'ALGORITHM & GROWTH' },
    tag: 'growth',
    readTime: { id: '4 Menit Baca', en: '4 Min Read' },
    date: '2026-11-20',
    title: {
      id: 'Cara Kerja Algoritma Threads 2026: Kenapa Reply Velocity 15 Menit Pertama Menentukan Jangkauan',
      en: 'How the 2026 Threads Algorithm Works: Why First-15-Minute Reply Velocity Drives Reach'
    },
    excerpt: {
      id: 'Bedah sinyal distribusi Threads dan bagaimana membalas komentar lebih cepat mendongkrak tayangan organik hingga 3x lipat.',
      en: 'Breakdown of Threads distribution signals and how rapid comment replies multiply organic impressions up to 3x.'
    },
    sections: [
      {
        heading: {
          id: '1. Threads Mengukur Percakapan, Bukan Sekadar Like Pasif',
          en: '1. Threads Ranks Conversations, Not Passive Likes'
        },
        body: {
          id: [
            'Berbeda dari platform visual yang mengandalkan durasi tonton, mesin rekomendasi Threads memberi bobot tertinggi pada kedalaman balasan (reply depth) dan kecepatan interaksi di 15–30 menit pertama setelah post tayang.',
            'Ketika sebuah post memicu komentar dan pemilik akun langsung membalas dengan pertanyaan lanjutan, sistem membaca utas tersebut sebagai diskusi aktif yang layak didorong ke tab For You.'
          ],
          en: [
            'Unlike visual feeds driven by watch time, Threads places its highest ranking weight on reply depth and interaction velocity within the first 15–30 minutes after publishing.',
            'When a post sparks comments and the author replies promptly with a follow-up angle, the ranking system treats the thread as an active conversation worth distributing to For You feeds.'
          ]
        }
      },
      {
        heading: {
          id: '2. Masalah Klasik Kreator: Telat Balas Karena Sibuk',
          en: '2. The Creator Bottleneck: Late Replies Kill Momentum'
        },
        body: {
          id: [
            'Sebagian besar kreator memposting di jam sibuk lalu menutup aplikasi. Komentar yang masuk baru dibalas 4–6 jam kemudian saat momentum distribusi sudah turun.',
            'Dengan Smart Inbox Ixiera yang ditenagai Groq LPU, setiap komentar dan mention otomatis dikategorikan (Pertanyaan, Pujian, Netral, Spam) dan disiapkan draf balasannya dalam hitungan milidetik sesuai gaya bahasamu.'
          ],
          en: [
            'Most creators publish during peak hours and close the app, replying 4–6 hours later after the distribution window has already decayed.',
            'With Ixiera Smart Inbox powered by Groq LPU, incoming comments and public mentions are automatically sorted (Question, Praise, Neutral, Spam) with sub-second reply drafts matched to your tone.'
          ]
        }
      }
    ]
  },
  {
    slug: 'framework-konten-3-hari-threads',
    category: { id: 'COPYWRITING & JUALAN', en: 'COPYWRITING & SALES' },
    tag: 'copywriting',
    readTime: { id: '5 Menit Baca', en: '5 Min Read' },
    date: '2026-11-21',
    title: {
      id: 'Framework Konten 3-Hari: Edukasi, Bukti Sosial, dan Soft-Selling Tanpa Terlihat Spam',
      en: 'The 3-Day Content Framework: Education, Social Proof, and Soft-Selling Without Sounding Spammy'
    },
    excerpt: {
      id: 'Pola rotasi konten harian yang dipakai kreator digital dan founder SaaS untuk mengubah pembaca pasif menjadi pembeli.',
      en: 'The daily content rotation used by digital creators and SaaS founders to convert passive readers into paying customers.'
    },
    sections: [
      {
        heading: {
          id: 'Pola Rotasi 3 Hari yang Terbukti Konsisten',
          en: 'A Repeatable 3-Day Rotation That Converts'
        },
        body: {
          id: [
            'Hari 1 (Insight & Masalah): Bongkar satu kesalahan spesifik yang sering dilakukan audiensmu dan berikan langkah perbaikan cepat. Tujuannya membangun otoritas dan memancing simpan/repost.',
            'Hari 2 (Bukti Nyata & Proses): Bagikan tangkapan layar hasil kerja, eksperimen, atau cerita di balik layar. Orang membeli dari proses yang transparan.',
            'Hari 3 (Undangan & Solusi): Hubungkan masalah di Hari 1 dengan produk/jasamu menggunakan CTA ringan di akhir utas.'
          ],
          en: [
            'Day 1 (Insight & Problem): Break down one specific mistake your audience makes and show a practical fix. This builds authority and earns reposts.',
            'Day 2 (Proof & Process): Share real metrics, experiments, or behind-the-scenes lessons. People buy from transparent execution.',
            'Day 3 (Invitation & Offer): Connect Day 1’s problem directly to your product or service with a low-friction CTA.'
          ]
        },
        copyBox: {
          label: { id: 'Prompt AI Content Planner (Siap Pakai)', en: 'AI Content Planner Prompt (Ready to Use)' },
          content: 'Buatkan rencana konten Threads 3 hari untuk niche [ISI NICHE KAMU]. Hari 1: Edukasi kesalahan umum + solusi taktis. Hari 2: Studi kasus / angka nyata. Hari 3: Soft-selling ke [NAMA PRODUK] dengan CTA ajakan diskusi di komentar. Gaya bahasa lugas, tanpa basa-basi.'
        }
      }
    ]
  },
  {
    slug: '30-hook-threads-dan-prompt-knowledge-base',
    category: { id: 'FREE RESOURCE', en: 'FREE RESOURCE' },
    tag: 'resource',
    readTime: { id: 'Template Siap Pakai', en: 'Ready-to-Use Templates' },
    date: '2026-11-22',
    isResource: true,
    title: {
      id: 'Free Playbook: 15 Hook Pembuka Threads Teruji & Template Aturan Knowledge Base Anti-Kaku',
      en: 'Free Playbook: 15 Proven Threads Opening Hooks & Anti-Generic Knowledge Base Rules'
    },
    excerpt: {
      id: 'Kumpulan formula baris pertama penahan scroll beserta template aturan gaya bahasa yang bisa langsung kamu tempel ke Ixiera.',
      en: 'High-retention first-line formulas plus brand voice rules ready to paste straight into your Ixiera Knowledge Base.'
    },
    sections: [
      {
        heading: {
          id: '15 Formula Hook Penahan Scroll (Tinggal Isi Bagian Kurung)',
          en: '15 Scroll-Stopping Hook Formulas (Fill in the Blanks)'
        },
        body: {
          id: [
            'Data analitik menunjukkan 70% keputusan pembaca untuk berhenti scroll ditentukan oleh 2 baris pertama sebelum tombol "Lihat lainnya". Gunakan pola berikut di Composer Ixiera:'
          ],
          en: [
            'Analytics show 70% of a reader’s decision to stop scrolling happens in the first 2 lines. Use these templates inside Ixiera Composer:'
          ]
        },
        copyBox: {
          label: { id: 'Salin & Tempel ke Composer Ixiera', en: 'Copy & Paste into Ixiera Composer' },
          content: `1. Kesalahan terbesar [TARGET AUDIENS] saat baru mulai [AKTIVITAS]:
2. Saya menghabiskan [WAKTU/BIAYA] untuk menguji [TOPIK]. Ini 3 hal yang benar-benar berhasil:
3. Berhenti melakukan [KEBIASAAN LAMA] kalau targetmu [HASIL YANG DIINGINKAN]. Ganti dengan ini:
4. Unpopular opinion di industri [NICHE]: [PENDAPAT TEGAS KAMU].
5. Cara saya menyelesaikan [MASALAH] dalam [WAKTU SINGKAT] tanpa [HAMBATAN UMUM]:
6. Kalau besok saya harus mulai dari nol di [BIDANG], ini 4 langkah pertama yang bakal saya ambil:
7. Banyak yang tanya kenapa [HASIL KAMU] bisa stabil. Jawabannya bukan bakat, tapi sistem ini:
8. 5 tanda [PROYEK/AKUN] kamu sebenarnya sudah siap naik kelas, tapi ketahan di satu hal:`
        }
      },
      {
        heading: {
          id: 'Template Aturan Knowledge Base (Biar Balasan AI Terasa Seperti Kamu)',
          en: 'Knowledge Base Persona Template (Make AI Replies Sound Like You)'
        },
        body: {
          id: [
            'Tempel aturan di bawah ini ke menu Pengaturan -> Knowledge Base di dashboard Ixiera agar Gemini dan Groq selalu mengikuti karakter brand kamu:'
          ],
          en: [
            'Paste the rules below into Settings -> Knowledge Base inside Ixiera so Gemini and Groq strictly follow your brand voice:'
          ]
        },
        copyBox: {
          label: { id: 'Salin & Tempel ke Knowledge Base Ixiera', en: 'Copy & Paste into Ixiera Knowledge Base' },
          content: `ATURAN GAYA BAHASA & BALASAN:
- Gunakan bahasa Indonesia santai tapi profesional (panggil audiens dengan "kamu" atau "kak" sesuai konteks).
- Jawaban maksimal 2-3 kalimat padat. Langsung ke inti jawaban tanpa pembukaan klise seperti "Halo, terima kasih telah bertanya!".
- Jika ada yang menanyakan harga atau cara mulai, arahkan untuk mencoba Free Trial 7 hari langsung di https://ixiera.online.
- Jangan pernah mengarang fitur atau diskon yang tidak tertulis di dokumen Knowledge Base ini.`
        }
      }
    ]
  },
  {
    slug: 'riset-trending-topics-dan-cross-post-instagram',
    category: { id: 'STRATEGI MULTI-CHANNEL', en: 'MULTI-CHANNEL STRATEGY' },
    tag: 'growth',
    readTime: { id: '4 Menit Baca', en: '4 Min Read' },
    date: '2026-11-23',
    title: {
      id: 'Strategi Multi-Channel: Memanfaatkan Trending Topics, Location Tagging & Cross-Post Instagram',
      en: 'Multi-Channel Strategy: Leveraging Trending Topics, Location Tagging & Instagram Cross-Posting'
    },
    excerpt: {
      id: 'Cara menjangkau audiens baru lewat topik yang sedang naik daun dan mendistribusikan satu konten ke Threads sekaligus Instagram.',
      en: 'How to capture new audiences through live trending topics and distribute one post across Threads and Instagram simultaneously.'
    },
    sections: [
      {
        heading: {
          id: '1. Masuk ke Percakapan yang Sudah Punya Traffic',
          en: '1. Join Conversations That Already Have Traffic'
        },
        body: {
          id: [
            'Menulis dari nol tanpa konteks sering membuat post sepi pembaca. Melalui fitur Trending Topics & Keyword Search di Ixiera, kamu bisa melihat topik yang sedang ramai dibahas hari ini lalu menyumbangkan sudut pandang dari niche-mu.',
            'Gunakan Profile Discovery untuk memantau format tulisan kreator top di topik tersebut tanpa harus berpindah tab.'
          ],
          en: [
            'Writing in a vacuum limits discovery. Using Trending Topics & Keyword Search inside Ixiera, you can spot active conversations today and contribute your niche perspective.',
            'Use Profile Discovery to inspect creator benchmarks in that topic without switching tabs.'
          ]
        }
      },
      {
        heading: {
          id: '2. Satu Kali Tulis: Tayang di Threads + Instagram dengan Tag Lokasi',
          en: '2. Write Once: Publish to Threads + Instagram with Location Tags'
        },
        body: {
          id: [
            'Untuk bisnis lokal, event, maupun personal brand, menambahkan Location Tag membantu konten muncul di pencarian berbasis lokasi. Aktifkan toggle Share to Instagram di Composer Ixiera agar post otomatis terdistribusi ke feed Instagram tanpa kerja dua kali.'
          ],
          en: [
            'For local businesses, events, and personal brands, attaching a verified Location Tag boosts regional discovery. Toggle Share to Instagram in Ixiera Composer to cross-post automatically without duplicate effort.'
          ]
        }
      }
    ]
  }
]
