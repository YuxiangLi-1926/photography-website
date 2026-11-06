export const site = {
  name: 'Yuxiang Li Photography',
  description: 'Personal photography portfolio website',
};

export const navigationLinks = [
  { title: 'Work', href: '/work/' },
  { title: 'Contact', href: '/contact/' },
];

export const gallerySections = [
  {
    title: 'Event',
    href: '/event/',
    description: 'Placeholder for event photography collections.',
  },
  {
    title: 'Nightlife',
    href: '/nightlife/',
    description: 'Placeholder for nightlife photography collections.',
  },
  {
    title: 'Food',
    href: '/food/',
    description: 'Placeholder for food photography collections.',
  },
  {
    title: 'Portrait',
    href: '/portrait/',
    description: 'Placeholder for portrait photography collections.',
  },
  {
    title: 'Cars',
    href: '/cars/',
    description: 'Placeholder for automotive photography collections.',
  },
  {
    title: 'Her',
    href: '/her/',
    description: 'Placeholder for a dedicated personal gallery.',
  },
  {
    title: 'My Work',
    href: '/my-work/',
    description: 'Placeholder for selected work and featured projects.',
  },
];

export const homepageCategories = [
  {
    title: 'Event',
    category: 'event',
    href: '/event/',
    description: 'Atmosphere, arrivals, gatherings, and the shape of a night.',
  },
  {
    title: 'Nightlife',
    category: 'nightlife',
    href: '/nightlife/',
    description: 'Low light, movement, music, and the pulse after dark.',
  },
  {
    title: 'Food',
    category: 'food',
    href: '/food/',
    description: 'Restaurants, tables, textures, and the rituals around food.',
  },
  {
    title: 'Portrait',
    category: 'portrait',
    href: '/portrait/',
    description: 'Faces, presence, mood, and quiet personal detail.',
  },
  {
    title: 'Cars',
    category: 'cars',
    href: '/cars/',
    description: 'Form, speed, surfaces, and automotive character.',
  },
] as const;

export const contactLinks = [
  { title: 'Email', href: 'mailto:dhrlyx@gmail.com' },
];
