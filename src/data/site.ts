export const site = {
  name: 'Yuxiang Li Photography',
  description: 'Personal photography portfolio website',
};

export const navigationLinks = [
  { title: 'Work', href: '/work/' },
  { title: 'Contact', href: '/contact/' },
];

export const gallerySections = [
  { title: 'People', href: '/portrait/', description: 'Portraits and graduation stories.' },
  { title: 'Moments', href: '/moments/', description: 'Events, nightlife and campaigns.' },
  { title: 'Food', href: '/food/', description: 'Food photography.' },
  { title: 'Places', href: '/places/', description: 'Places, journeys and personal stories.' },
  { title: 'Sweetie', href: '/sweetie/', description: 'Dogs, cats and their little moments.' },
];

export const homepageCategories = [
  { title: 'People', category: 'portrait', href: '/portrait/', description: 'Portraits and graduation stories.' },
  { title: 'Moments', category: 'event', href: '/moments/', description: 'Events, nightlife and campaigns.' },
  { title: 'Food', category: 'food', href: '/food/', description: 'Food photography.' },
  { title: 'Places', category: 'my-work', href: '/places/', description: 'Places, journeys and personal stories.' },
  { title: 'Sweetie', category: 'sweetie', href: '/sweetie/', description: 'Dogs, cats and their little moments.' },
] as const;

export const contactLinks = [
  { title: 'Email', href: 'mailto:dhrlyx@gmail.com' },
];
