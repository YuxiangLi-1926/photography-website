import { mediaConfig } from '../config/media';
import { galleryManifest } from '../data/galleryManifest';
import type { GalleryCategory, Photo } from '../data/galleryTypes';

export const photos = sortPhotosByOrder(galleryManifest);

export function getImageUrl(key: string): string {
  const baseUrl = (import.meta.env.PUBLIC_PORTFOLIO_MEDIA_URL || mediaConfig.r2BaseUrl).replace(/\/$/, '');
  const objectKey = key.replace(/^\//, '');

  return `${baseUrl}/${objectKey}`;
}

export function sortPhotosByOrder(photoList: readonly Photo[]): Photo[] {
  return [...photoList].sort((a, b) => a.order - b.order);
}

export function getPhotosByCategory(category: GalleryCategory): Photo[] {
  return sortPhotosByOrder(
    galleryManifest.filter((photo) => photo.category === category),
  );
}

export function getFeaturedPhotos(): Photo[] {
  return sortPhotosByOrder(galleryManifest.filter((photo) => photo.featured));
}

export function getFeaturedPhotosByCategory(category: GalleryCategory): Photo[] {
  return sortPhotosByOrder(
    galleryManifest.filter((photo) => photo.category === category && photo.featured),
  );
}

export function getFirstFeaturedPhotoByCategory(
  category: GalleryCategory,
): Photo | undefined {
  return getFeaturedPhotosByCategory(category)[0];
}
