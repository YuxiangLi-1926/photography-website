export const galleryCategories = [
  'event',
  'nightlife',
  'food',
  'portrait',
  'cars',
  'her',
  'my-work',
] as const;

export type GalleryCategory = (typeof galleryCategories)[number];

export interface Photo {
  id: string;
  key: string;
  category: GalleryCategory;
  project?: string;
  year?: number;
  width: number;
  height: number;
  altZh: string;
  altEn: string;
  featured: boolean;
  order: number;
}
